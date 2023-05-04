import RPi.GPIO as GPIO

from relays.models import Channel
from relays.models import Relay


def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    for relay in Relay.objects.all():
        GPIO.setup(relay.channel.pin, GPIO.OUT)
    GPIO.cleanup()


def set_channel_state(channel: Channel, state: bool):
    GPIO.output(channel.pin, GPIO.LOW if state else GPIO.HIGH)
