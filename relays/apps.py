from django.apps import AppConfig


class RelaysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relays'

    def ready(self):
        from . import signals
