from django.apps import AppConfig


class RelaysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relays'
    audit_log_pagination_page_size = 10

    def ready(self):
        from . import signals

        # GPIO related initialization
        #from relays.utils.gpio import init_GPIO

        #init_GPIO()
