import time

from relays.models import Channel
from relays.models import Relay
from relays.utils.gpio import set_channel_state
from smart_relays.celery import app


@app.task
def test_channel(channel_id: int):
    channel: Channel = Channel.objects.get(pk=channel_id)
    for _ in range(3):
        toggle_relay.delay(channel.relay.id)
        time.sleep(.5)
        toggle_relay.delay(channel.relay.id)
        time.sleep(.5)


@app.task
def toggle_relay(relay_id: int):
    relay: Relay = Relay.objects.get(pk=relay_id)

    set_channel_state(relay.channel, True)
    time.sleep(.1)
    set_channel_state(relay.channel, False)
