import json

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView

from accounts.forms import UserCreateForm
from accounts.utils.access.user_relay_access_tests import owner_or_shared, owner_or_full_access, \
    owner_or_at_least_control, superuser, owner_or_full_access_or_superuser, owner_or_shared_or_superuser
from relays.forms import RelayUpdateForm, RelayCreateForm, ShareRelayForm, ChannelForm
from relays.models import Relay, RelayStateChange, RelayCreateRecord, RelayUpdateRecord, UserRelayShare, \
    RelayShareRecord, Channel
from smart_relays.models import ApplicationData
from smart_relays.utils.config import get_relays_config, get_project_config
from smart_relays.utils.template import push_form_errors_to_messages
from smart_relays.views import SmartRelaysView


class WizardView(SmartRelaysView, TemplateView):
    template_name = 'wizard.html'
    title = 'Setup Wizard'
    login_required = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['wizard_data'] = ApplicationData.objects.get(key='setup_wizard').data

        return context

    def get(self, request, *args, **kwargs):
        if ApplicationData.objects.get(key='setup_wizard').data['completed']:
            return HttpResponseRedirect(get_project_config().default_page)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        wizard_data = ApplicationData.objects.get(key='setup_wizard')
        current_step = int(request.POST.get('step'))
        match current_step:
            case 0:
                return self.__step_0_handler(request, wizard_data)
            case 1:
                return self.__step_1_handler(request, wizard_data)
            case 2:
                return self.__setp_2_handler(request, wizard_data)
        return HttpResponseRedirect(request.path)

    def __step_0_handler(self, request: HttpRequest, wizard_data: ApplicationData):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            admin = form.save()

            admin.is_superuser = True
            admin.is_staff = True
            admin.save()

            login(request, admin)

            wizard_data.data['step'] = 1
            wizard_data.save()
        else:
            push_form_errors_to_messages(request, form)
        return HttpResponseRedirect(request.path)

    def __step_1_handler(self, request: HttpRequest, wizard_data: ApplicationData):
        for pin in [pin for pin in list(json.loads(str(request.POST['pins']))) if pin]:
            Channel.objects.create(pin=pin)
        wizard_data.data['step'] = 2
        wizard_data.save()
        return HttpResponseRedirect(request.path)

    def __setp_2_handler(self, request: HttpRequest, wizard_data: ApplicationData):
        wizard_data.data = {'completed': True}
        wizard_data.save()
        return HttpResponseRedirect(request.path)


def test_relay_channel(request: HttpRequest):
    pin = int(request.GET.get('pin') or 0)
    from relays.tasks import test_pin
    test_pin.delay(pin)
    return HttpResponse()


# ----------------------------------------
# Relay Views
# ----------------------------------------

class RelayListView(SmartRelaysView, ListView):
    template_name = 'relay_list.html'
    title = 'Relays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = RelayCreateForm(initial={'user': self.request.user})
        return context

    def get_queryset(self):
        return Relay.objects.for_user(self.request.user)


class RelayDetailView(SmartRelaysView, DetailView):
    model = Relay
    template_name = 'relay_detail.html'

    def test_func(self, request: HttpRequest):
        return owner_or_shared_or_superuser(self.request.user, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state_history'] = {
            str(state_change.timestamp): state_change.new_state for state_change in
            RelayStateChange.objects.for_relay(self.get_object())
        }

        context['share_form'] = ShareRelayForm(
            self.get_object().get_possible_recipients(),
            initial={'relay': self.get_object()}
        )
        context['relay_shares'] = UserRelayShare.objects.for_relay(self.get_object())

        default_audit_log_limit = get_relays_config().audit_log_pagination_page_size
        audit_log_limit = int(self.request.GET.get('audit_log_limit', default_audit_log_limit))
        context['audit_log_limit'] = audit_log_limit, default_audit_log_limit
        context['audit_log'] = self.get_object().get_audit_log(audit_log_limit)

        context['permissions'] = {
            'sharing': owner_or_full_access_or_superuser(self.request.user, self.get_object()),
            'audit_log': owner_or_full_access_or_superuser(self.request.user, self.get_object()),
        }

        context['quick_scheduling'] = [
            ('5 min', 5 * 60, 'is-info'),
            ('15 min', 15 * 60, 'is-info'),
            ('30 min', 30 * 60, 'is-info'),
            ('1 hour', 60 * 60, 'is-link'),
            ('6 hours', 6 * 60 * 60, 'is-link'),
            ('12 hours', 12 * 60 * 60, 'is-link'),
            ('Tomorrow (this time)', 24 * 60 * 60, 'is-primary'),
        ]

        return context

    def get_title(self):
        return self.object.name


class RelayUpdateView(SmartRelaysView, UpdateView):
    model = Relay
    form_class = RelayUpdateForm
    template_name = 'relay_form.html'
    title = 'Relay update'

    def test_func(self, request: HttpRequest):
        return owner_or_full_access_or_superuser(self.request.user, self.get_object())

    def get_page_subtitle(self):
        return self.object

    def post(self, request, *args, **kwargs):
        # Put this request into a queue so that the save handler can have access to it
        Relay.update_requests.put(request)
        return super().post(request, *args, **kwargs)


class RelayCreateView(SmartRelaysView, CreateView):
    http_method_names = ['post']
    model = Relay
    form_class = RelayCreateForm
    success_url = reverse_lazy('relays:relay-list')

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, error)
                else:
                    messages.error(self.request, f'<b>{field}</b>: {error}')
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        # Put this request into a queue so that the save handler can have access to it
        Relay.update_requests.put(request)
        return super().post(request, *args, **kwargs)


class RelayDeleteView(SmartRelaysView, DeleteView):
    http_method_names = ('post',)
    model = Relay
    success_url = reverse_lazy('relays:relay-list')

    def test_func(self, request: HttpRequest):
        return owner_or_full_access_or_superuser(self.request.user, self.get_object())


class RelayChangeStateView(SmartRelaysView, View):
    relay: Relay = None

    def handle_test_fail(self, request) -> HttpResponse:
        return HttpResponseForbidden()

    def test_func(self, request: HttpRequest):
        self.relay = Relay.objects.get(pk=request.resolver_match.kwargs['pk'])
        return owner_or_at_least_control(request.user, self.relay)

    def post(self, request, *args, **kwargs):
        try:
            delay = int(request.POST['delay'])
        except KeyError:
            delay = 0
        self.relay.toggle(request, delay)
        return HttpResponse()


# ----------------------------------------
# Channel Views
# ----------------------------------------
class ChannelListView(SmartRelaysView, ListView):
    template_name = 'channel_list.html'
    title = 'Channels'
    model = Channel

    def test_func(self, request: HttpRequest):
        return superuser(request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['create_form'] = ChannelForm()

        return context


class ChannelUpdateView(SmartRelaysView, UpdateView):
    model = Channel
    form_class = ChannelForm
    template_name = 'channel_form.html'
    title = 'Channel update'
    success_url = reverse_lazy('relays:channel-list')

    def test_func(self, request: HttpRequest):
        return superuser(request.user)

    def get_page_subtitle(self):
        return self.object


class ChannelCreateView(SmartRelaysView, CreateView):
    http_method_names = ('post',)
    model = Channel
    form_class = ChannelForm
    success_url = reverse_lazy('relays:channel-list')

    def test_func(self, request: HttpRequest):
        return superuser(request.user)

    def form_invalid(self, form):
        push_form_errors_to_messages(self.request, form)
        return redirect(self.success_url)


class ChannelDeleteView(SmartRelaysView, DeleteView):
    http_method_names = ('post',)
    model = Channel
    success_url = reverse_lazy('relays:channel-list')

    def test_func(self, request: HttpRequest):
        return superuser(self.request.user)


class ChannelTestView(SmartRelaysView, View):
    def test_func(self, request: HttpRequest):
        return superuser(request.user)

    def get(self, request, *args, **kwargs):
        from relays.tasks import test_channel
        channel: Channel = Channel.objects.get(pk=kwargs['pk'])

        test_channel.delay(channel.pk)

        messages.info(request, f'Testing channel <b>{channel}</b>...')

        return HttpResponseRedirect(reverse('relays:channel-list'))


# ----------------------------------------
# Audit Log Views
# ----------------------------------------


class AuditLogView(SmartRelaysView, ListView):
    template_name = 'audit_log.html'
    title = 'Audit Log'
    paginate_by = 10

    def test_func(self, request: HttpRequest):
        return superuser(request.user)

    def get_queryset(self):
        create_records = list(RelayCreateRecord.objects.all())
        update_records = list(RelayUpdateRecord.objects.all())
        state_change_records = list(RelayStateChange.objects.all())
        relay_share_records = list(RelayShareRecord.objects.all())

        logs = sorted(
            create_records + update_records + state_change_records + relay_share_records,
            key=lambda log: log.timestamp,
            reverse=True
        )
        return logs


# ----------------------------------------
# Relay Sharing Views
# ----------------------------------------

class CreateRelayShareView(SmartRelaysView, CreateView):
    http_method_names = ('post',)
    form_class = ShareRelayForm


class RevokeRelayShareView(SmartRelaysView, DeleteView):
    http_method_names = ('post',)
    model = UserRelayShare

    def get_success_url(self):
        print(RelayShareRecord.objects.get(pk=self.get_object().pk))
        if owner_or_full_access_or_superuser(self.request.user, self.get_object().relay):
            return reverse('relays:relay-detail', kwargs={'pk': self.get_object().relay.pk})
        else:
            return reverse(get_project_config().default_page)

    def test_func(self, request: HttpRequest):
        return owner_or_full_access_or_superuser(self.request.user, self.get_object().relay)


class RelayShareUpdateView(SmartRelaysView, UpdateView):
    http_method_names = ('post',)
    model = UserRelayShare
    fields = ('permission_level',)

    def test_func(self, request: HttpRequest):
        return owner_or_full_access_or_superuser(self.request.user, self.get_object().relay)
