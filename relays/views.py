from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from relays.models import Relay, RelayAuditRecord, RelayStateChange
from relays.utils.relay import last_known_relay_state, last_know_relay_state_change_timestamp
from smart_relays.views import SmartRelaysView


class RelayListView(LoginRequiredMixin, SmartRelaysView, ListView):
    queryset = Relay.objects.all()
    template_name = 'relay_list.html'
    title = 'Relays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

    def get_title(self):
        return self.object.name


class RelayUpdateView(UpdateView):
    model = Relay
    template_name = 'relay_form.html'
    fields = ('name', 'description')


class RelayDeleteView(DeleteView):
    model = Relay
