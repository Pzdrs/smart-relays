from django.contrib import messages
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView, CreateView

from relays.forms import RelayUpdateForm, RelayCreateForm, ShareRelayForm
from relays.models import Relay, RelayStateChange, RelayCreateRecord, RelayUpdateRecord, UserRelayShare
from relays.utils.relay import relay_slots_breakdown
from relays.utils.template import get_progress_bar_color
from relays.utils.user_access_tests import owner_or_full_access, owner_or_at_least_control, owner_or_shared
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
        context['audit_log'] = self.get_object().get_audit_log()
        context['relay_shares'] = UserRelayShare.objects.for_relay(self.get_object())

        context['share_form'] = ShareRelayForm(
            self.get_object().get_possible_recipients(),
            initial={'relay': self.get_object()}
        )
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
        RelayStateChange.objects.toggle(self.relay, request.user)
        return HttpResponse()


# ----------------------------------------
# Audit Log Views
# ----------------------------------------


class AuditLogView(SmartRelaysView, TemplateView):
    template_name = 'audit_log.html'
    title = 'Audit Log'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_records = [record for record in RelayCreateRecord.objects.all()]
        update_records = [record for record in RelayUpdateRecord.objects.all()]
        state_change_records = [record for record in RelayStateChange.objects.all()]
        context['logs'] = sorted(
            create_records + update_records + state_change_records,
            key=lambda log: log.timestamp,
            reverse=True
        )
        return context


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
