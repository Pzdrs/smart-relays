from django.db.models.signals import post_save
from django.dispatch import receiver

from relays.models import Relay, RelayCreateLog


@receiver(post_save, sender=Relay)
def post_relay_create_signal(instance: Relay, created: bool, **kwargs):
    if created:
        create_log = RelayCreateLog(relay=instance, user=Relay.get_last_update_user())
        create_log.save()
