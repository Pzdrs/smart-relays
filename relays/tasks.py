import time

import RPi.GPIO as GPIO

from relays.models import Channel
from relays.models import Relay
from smart_relays.celery import app


@app.task
def test_channel(channel_id: int):
    channel: Channel = Channel.objects.get(pk=channel_id)
    for _ in range(3):
        GPIO.output(channel.pin, GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(channel.pin, GPIO.HIGH)
        time.sleep(0.5)
    GPIO.cleanup()


@app.task
def toggle_relay(relay_id: int):
    relay: Relay = Relay.objects.get(pk=relay_id)
    relay.toggle()


@app.task
def sync_channels():
    for relay in Relay.objects.synchronized():
        relay.channel.synchronize()
