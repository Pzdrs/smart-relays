from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from relays.models import Relay, RelayAuditRecord
from smart_relays.views import SmartRelaysView


class RelayListView(SmartRelaysView, ListView):
    queryset = Relay.objects.all()
    template_name = 'relay_list.html'
    title = 'Relays'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class RelayDetailView(SmartRelaysView, DetailView):
    model = Relay
    template_name = 'login.html'

    def get_title(self):
        return self.object.name


class RelayUpdateView(UpdateView):
    model = Relay


class RelayDeleteView(DeleteView):
    model = Relay
