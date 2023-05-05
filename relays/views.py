from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from accounts.utils.access.user_relay_access_tests import owner_or_shared, owner_or_full_access, \
    owner_or_at_least_control, superuser
from relays.forms import RelayUpdateForm, RelayCreateForm, ShareRelayForm, ChannelForm
from relays.models import Relay, RelayStateChange, RelayCreateRecord, RelayUpdateRecord, UserRelayShare, \
    RelayShareRecord, Channel
from relays.utils.relay import relay_slots_breakdown
from relays.utils.template import get_progress_bar_color
from smart_relays.utils.config import get_relays_config
from smart_relays.utils.template import push_form_errors_to_messages
from smart_relays.views import SmartRelaysView


# ----------------------------------------
# Relay Views
# ----------------------------------------

class RelayListView(SmartRelaysView, ListView):
    template_name = 'relay_list.html'
    title = 'Relays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slots_breakdown = relay_slots_breakdown()

        context['slots_max'] = slots_breakdown[0]
        context['slots_used'] = slots_breakdown[1]
        context['slots_left'] = slots_breakdown[2]

        context['progress_color'] = get_progress_bar_color(slots_breakdown[1] / slots_breakdown[0])

        context['create_form'] = RelayCreateForm(initial={'user': self.request.user})
        return context

    def get_queryset(self):
        return Relay.objects.for_user(self.request.user)


class RelayDetailView(SmartRelaysView, DetailView):
    model = Relay
    template_name = 'relay_detail.html'

    def test_func(self, request: HttpRequest):
        return owner_or_shared(self.request.user, self.get_object())

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

        return context

    def get_title(self):
        return self.object.name


class RelayUpdateView(SmartRelaysView, UpdateView):
    model = Relay
    form_class = RelayUpdateForm
    template_name = 'relay_form.html'
    title = 'Relay update'

    def test_func(self, request: HttpRequest):
        return owner_or_full_access(self.request.user, self.get_object())

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
        return owner_or_full_access(self.request.user, self.get_object())


class RelayChangeStateView(SmartRelaysView, View):
    relay: Relay = None

    def handle_test_fail(self, request) -> HttpResponse:
        return HttpResponseForbidden()

    def test_func(self, request: HttpRequest):
        self.relay = Relay.objects.get(pk=request.resolver_match.kwargs['pk'])
        return owner_or_at_least_control(request.user, self.relay)

    def post(self, request, *args, **kwargs):
        self.relay.toggle(request)
        return HttpResponse()


# ----------------------------------------
# Channel Views
# ----------------------------------------
class ChannelListView(SmartRelaysView, ListView):
    template_name = 'channel_list.html'
    title = 'Channels'
    model = Channel

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
        return reverse('relays:relay-detail', kwargs={'pk': self.get_object().relay.pk}) + '#sharing'

    def test_func(self, request: HttpRequest):
        return owner_or_full_access(self.request.user, self.get_object().relay)


class RelayShareUpdateView(SmartRelaysView, UpdateView):
    http_method_names = ('post',)
    model = UserRelayShare
    fields = ('permission_level',)

    def test_func(self, request: HttpRequest):
        return owner_or_full_access(self.request.user, self.get_object().relay)
