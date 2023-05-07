import RPi.GPIO as GPIO

from relays.models import Channel


def init_GPIO():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for channel in Channel.objects.all():
        init_channel(channel)


def init_channel(channel: Channel):
    GPIO.setup(channel.pin, GPIO.OUT)
    GPIO.output(channel.pin, GPIO.HIGH)


def set_channel_state(pin: int, state: bool):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW if state else GPIO.HIGH)
