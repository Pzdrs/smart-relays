from django.apps import AppConfig

from relays.tasks import sync_channels


class RelaysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relays'
    audit_log_pagination_page_size = 10

    def ready(self):
        from . import signals
        sync_channels.delay()
