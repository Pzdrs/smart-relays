from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from relays.models import Relay, RelayCreateRecord


@receiver(post_save, sender=Relay)
def post_relay_create_signal(instance: Relay, created: bool, **kwargs):
    if created:
        create_log = RelayCreateRecord(relay=instance, user=Relay.get_last_update_user())
        create_log.save()


@receiver(post_migrate)
def init_GPIO_post_migrate():
    from relays.utils.gpio import init_GPIO
    init_GPIO()
