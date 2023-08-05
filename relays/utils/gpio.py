import logging

from relays.models import Channel
from relays.utils._platform import ON_SUPPORTED_PLATFORM

if ON_SUPPORTED_PLATFORM:
    import RPi.GPIO as GPIO


def init_GPIO():
    if not ON_SUPPORTED_PLATFORM:
        logging.warning('GPIO initialization skipped because platform is not supported')
        return
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for channel in Channel.objects.all():
        init_channel(channel)


def init_channel(channel: Channel):
    if not ON_SUPPORTED_PLATFORM:
        logging.warning('Channel initialization skipped because platform is not supported')
        return
    GPIO.setup(int(channel.pin), GPIO.OUT)
    GPIO.output(int(channel.pin), GPIO.HIGH)


def set_channel_state(pin: int, state: bool):
    if not ON_SUPPORTED_PLATFORM:
        logging.warning('Channel state change skipped because platform is not supported')
        return
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW if state else GPIO.HIGH)
