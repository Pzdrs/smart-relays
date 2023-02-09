from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from relays.models import Relay, RelayAuditRecord
from smart_relays.views import SmartRelaysView


class RelayListView(LoginRequiredMixin, SmartRelaysView, ListView):
    queryset = Relay.objects.all()
    template_name = 'relay_list.html'
    title = 'Relays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relay_states'] = {
            1: True,
            2: False,
            3: True,
            4: False,
        }
        return context


class RelayDetailView(SmartRelaysView, DetailView):
    model = Relay
    template_name = 'relay_detail.html'

    def get_title(self):
        return self.object.name


class RelayUpdateView(UpdateView):
    model = Relay


class RelayDeleteView(DeleteView):
    model = Relay
