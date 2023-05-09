import time

from accounts.models import User
from relays.models import Channel, RelayStateChange, Relay
from relays.utils.gpio import set_channel_state
from smart_relays.celery import app


@app.task
def test_channel(channel_id: int):
    channel: Channel = Channel.objects.get(pk=channel_id)
    test_pin(channel.pin)


@app.task
def test_pin(pin: int):
    for _ in range(3):
        __toggle_relay(pin)
        time.sleep(.5)
        __toggle_relay(pin)
        time.sleep(.5)


@app.task
def toggle_relay(relay_id: int, user_id: int):
    relay = Relay.objects.get(pk=relay_id)
    __toggle_relay(relay.channel.pin)
    RelayStateChange.objects.toggle(relay, User.objects.get(pk=user_id))


def __toggle_relay(pin: int):
    set_channel_state(pin, True)
    time.sleep(.1)
    set_channel_state(pin, False)
