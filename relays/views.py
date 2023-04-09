from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView, CreateView

from relays.forms import RelayUpdateForm, RelayCreateForm
from relays.models import Relay, RelayStateChange, RelayCreateLog, RelayUpdateLog
from relays.utils.relay import relay_slots_breakdown
from relays.utils.template import get_progress_bar_color
from smart_relays.views import SmartRelaysView


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state_history'] = RelayStateChange.objects.for_relay(self.object)
        context['audit_log'] = self.object.get_audit_log()
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


class RelayDeleteView(LoginRequiredMixin, DeleteView):
    http_method_names = ['post']
    model = Relay
    success_url = reverse_lazy('relays:relay-list')


class AuditLogView(SmartRelaysView, TemplateView):
    template_name = 'audit_log.html'
    title = 'Audit Log'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_logs = [log for log in RelayCreateLog.objects.all()]
        update_logs = [log for log in RelayUpdateLog.objects.all()]
        context['logs'] = sorted(create_logs + update_logs, key=lambda log: log.timestamp, reverse=True)
        return context
