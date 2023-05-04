import time

from relays.models import Channel
from relays.models import Relay
from relays.utils.gpio import toggle_channel
from smart_relays.celery import app


@app.task
def test_channel(channel_id: int):
    channel: Channel = Channel.objects.get(pk=channel_id)
    for _ in range(3):
        toggle_channel(channel)
        time.sleep(0.5)

        toggle_channel(channel)
        time.sleep(0.5)


@app.task
def toggle_relay(relay_id: int):
    relay: Relay = Relay.objects.get(pk=relay_id)
    toggle_channel(relay.channel)
    relay.toggle()


@app.task
def sync_channels():
    for relay in Relay.objects.synchronized():
        relay.channel.synchronize()
