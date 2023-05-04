from django.apps import AppConfig

from relays.signals import post_relay_create_signal
from relays.tasks import sync_channels


class RelaysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relays'
    audit_log_pagination_page_size = 10

    def ready(self):
        sync_channels.delay()
        post_relay_create_signal.connect(post_relay_create_signal, sender=self.get_model('Relay'))
