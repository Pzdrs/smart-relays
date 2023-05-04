import RPi.GPIO as GPIO

from relays.models import Channel


def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    for channel in Channel.objects.all():
        GPIO.setup(channel.pin, GPIO.OUT)


def set_channel_state(channel: Channel, state: bool):
    GPIO.output(channel.pin, GPIO.LOW if state else GPIO.HIGH)


def toggle_channel(channel: Channel):
    set_channel_state(channel, not GPIO.input(channel.pin))
