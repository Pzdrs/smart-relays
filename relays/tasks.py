import time

from relays.models import Channel, Relay
import RPi.GPIO as GPIO

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
    GPIO.setmode(GPIO.BCM)

    for relay in Relay.objects.all():
        GPIO.setup(relay.channel.pin, GPIO.OUT)
        current_state = relay.get_current_state()
        GPIO.output(relay.channel.pin, GPIO.LOW if current_state else GPIO.HIGH)
