from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from smart_relays.models import ApplicationData


class SetupWizardMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request: HttpRequest):
        setup_wizard_data = ApplicationData.objects.get_or_create(
            key='setup_wizard',
            data={'completed': False, 'step': 0}
        )
        if not setup_wizard_data.data['completed']:
            if request.path != reverse('relays:setup-wizard'):
                return redirect(reverse('relays:setup-wizard'))
        return self.get_response(request)
