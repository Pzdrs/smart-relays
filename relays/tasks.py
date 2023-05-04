import time

from relays.models import Channel
import RPi.GPIO as GPIO

from smart_relays.celery import app


@app.task
def test_channel(channel_id: int):
    channel: Channel = Channel.objects.get(pk=channel_id)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel.pin, GPIO.OUT)
    for _ in range(3):
        GPIO.output(channel.pin, GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(channel.pin, GPIO.HIGH)
        time.sleep(0.5)
