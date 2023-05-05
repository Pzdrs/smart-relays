from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from relays.models import Relay, RelayCreateRecord, Channel


@receiver(post_save, sender=Relay)
def post_relay_create_signal(instance: Relay, created: bool, **kwargs):
    if created:
        create_log = RelayCreateRecord(relay=instance, user=Relay.get_last_update_user())
        create_log.save()


@receiver(post_save, sender=Channel)
def channel_post_save(instance: Channel, **kwargs):
    """
    This signal is used to update the GPIO output when a channel is updated or created.
    """
    from relays.utils.gpio import init_channel
    init_channel(instance)
