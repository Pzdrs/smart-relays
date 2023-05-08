from django.apps import AppConfig
from django.urls import reverse_lazy

from smart_relays.utils.menu import Label, Link, Menu


class SmartRelaysConfig(AppConfig):
    name = 'smart_relays'
    default_title = 'Smart Relays'
    default_page = reverse_lazy('relays:relay-list')
    menu = Menu(
        Label('General'),
        Link('Relays', reverse_lazy('relays:relay-list')),
        Label('Advanced', lambda request: request.user.is_superuser),
        Link('Channels', reverse_lazy('relays:channel-list'), lambda request: request.user.is_superuser),
        Link('Users', reverse_lazy('accounts:user-management'), lambda request: request.user.is_superuser),
        Link('Audit Log', reverse_lazy('relays:audit-log'), lambda request: request.user.is_superuser),
        Label('Preferences'),
        Link('Change password', reverse_lazy('accounts:password-change')),
    )
