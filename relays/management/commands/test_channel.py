from django.core.management.base import BaseCommand

from relays.models import Channel
from relays.tasks import test_channel


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        test_channel(Channel.objects.get(pk=1))
