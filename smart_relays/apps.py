from django.apps import AppConfig
from django.urls import reverse_lazy

from smart_relays.utils.menu import Label, Link


class SmartRelaysConfig(AppConfig):
    name = 'smart_relays'
    default_title = 'Smart Relays'
    default_page = reverse_lazy('relays:relay-list')
    max_relays = 8
    menu = (
        Label('General'),
        Link('Relays', reverse_lazy('relays:relay-list')),
        Label('Advanced'),
        Link('Users', reverse_lazy('accounts:user-management')),
        Link('Audit Log', reverse_lazy('relays:audit-log')),
        Label('Preferences'),
        Link('Change password', reverse_lazy('accounts:password-change')),
    )
