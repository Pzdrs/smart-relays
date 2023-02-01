from django.apps import AppConfig
from django.urls import reverse_lazy

from smart_relays.utils.menu import Label, Link


class SmartRelaysConfig(AppConfig):
    name = 'smart_relays'
    default_title = 'Smart Relays'
    default_page = reverse_lazy('relays:relay-list')
    menu = [
        Label('General'),
        Link('Relays', reverse_lazy('relays:relay-list')),
        Label('Advanced')
    ]
