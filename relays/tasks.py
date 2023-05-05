import time

from accounts.models import User
from relays.models import Channel, RelayStateChange, Relay
from relays.utils.gpio import set_channel_state
from smart_relays.celery import app


@app.task
def test_channel(channel_id: int):
    channel: Channel = Channel.objects.get(pk=channel_id)
    for _ in range(3):
        toggle_relay(channel.id)
        time.sleep(.5)
        toggle_relay(channel.id)
        time.sleep(.5)


@app.task
def toggle_relay(channel_id: int):
    channel: Channel = Channel.objects.get(pk=channel_id)
    set_channel_state(channel, True)
    time.sleep(.1)
    set_channel_state(channel, False)


@app.task
def save_toggle_relay(relay_id: int, user_id: int):
    RelayStateChange.objects.toggle(Relay.objects.get(pk=relay_id), User.objects.get(pk=user_id))
