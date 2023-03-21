from relays.models import RelayStateChange, Relay
from smart_relays.utils.config import get_project_config


def last_known_relay_state(relay: Relay):
    last_state = RelayStateChange.objects.last_known_state(relay)
    return last_state.new_state if last_state else False


def last_know_relay_state_change_timestamp(relay: Relay):
    last_state = RelayStateChange.objects.last_known_state(relay)
    return last_state.timestamp if last_state else None


def relay_slots_breakdown() -> tuple[int, int, int]:
    max_relays = get_project_config().max_relays
    current_relays = Relay.objects.count()
    return max_relays, current_relays, max_relays - current_relays
