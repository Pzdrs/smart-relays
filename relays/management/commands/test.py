import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from accounts.models import User
from relays.models import Relay, RelayStateChange


class Command(BaseCommand):
    help = "Test command"

    def handle(self, *args, **options):
        relay = Relay.objects.all().first()
        timestamp = datetime.now()
        for i in range(25):
            # i need a timestamp that increases by a random value with every iteration to simulate a real world scenario
            timestamp += timedelta(hours=random.randint(1, 5)) + timedelta(minutes=random.randint(1, 60)) + timedelta(
                seconds=random.randint(1, 60))
            RelayStateChange.objects.create(relay=relay,user=User.objects.get(username='administrator'), new_state=not relay.get_current_state().new_state if relay.get_current_state() else True, timestamp=timestamp)
