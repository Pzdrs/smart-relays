import time

from relays.models import Channel
import RPi.GPIO as GPIO


def test_channel(channel: Channel):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel.pin, GPIO.OUT)
    for _ in range(3):
        GPIO.output(channel.pin, GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(channel.pin, GPIO.HIGH)
        time.sleep(0.5)
