from relays.models import Relay
from smart_relays.utils.config import get_project_config


def relay_slots_breakdown() -> tuple[int, int, int]:
    max_relays = get_project_config().max_relays
    current_relays = Relay.objects.count()
    return max_relays, current_relays, max_relays - current_relays
