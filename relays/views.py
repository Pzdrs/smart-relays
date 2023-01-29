from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from relays.models import Relay
from smart_relays.views import SmartRelaysView


class RelayListView(SmartRelaysView, ListView):
    queryset = Relay.objects.all()
    template_name = 'relay_list.html'
    title = 'Relays'


class RelayDetailView(SmartRelaysView, DetailView):
    model = Relay
    template_name = 'relay_detail.html'

    def get_title(self):
        return self.object.name


class RelayUpdateView(UpdateView):
    pass


class RelayDeleteView(DeleteView):
    pass
