from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView

from relays.forms import RelayUpdateForm
from relays.models import Relay, RelayStateChange, RelayCreateLog, RelayUpdateLog
from relays.utils.relay import last_known_relay_state, last_know_relay_state_change_timestamp
from smart_relays.views import SmartRelaysView


class RelayListView(LoginRequiredMixin, SmartRelaysView, ListView):
    queryset = Relay.objects.all()
    template_name = 'relay_list.html'
    title = 'Relays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slots'] = 4
        context['slots_used'] = 1
        context['slots_left'] = 3
        context['relay_states'] = {
            relay.pk: last_known_relay_state(relay)
            for relay in self.get_queryset()
        }
        context['last_relay_state_changes'] = {
            relay.pk: last_know_relay_state_change_timestamp(relay)
            for relay in self.get_queryset()
        }
        return context


class RelayDetailView(SmartRelaysView, DetailView):
    model = Relay
    template_name = 'relay_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state_history'] = RelayStateChange.objects.get_relay(self.object)
        return context

    def get_title(self):
        return self.object.name


class RelayUpdateView(SmartRelaysView, UpdateView):
    model = Relay
    form_class = RelayUpdateForm
    template_name = 'relay_form.html'
    title = 'Relay update'

    def get_page_subtitle(self):
        return self.object

    def post(self, request, *args, **kwargs):
        # Put this request into a queue so that the save handler can have access to it
        Relay._update_requests.put(request)
        return super().post(request, *args, **kwargs)


class RelayDeleteView(DeleteView):
    model = Relay


class AuditLogView(SmartRelaysView, TemplateView):
    template_name = 'audit_log.html'
    title = 'Audit Log'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_logs = [log for log in RelayCreateLog.objects.all()]
        update_logs = [log for log in RelayUpdateLog.objects.all()]
        context['logs'] = sorted(create_logs + update_logs, key=lambda log: log.timestamp, reverse=True)
        return context
