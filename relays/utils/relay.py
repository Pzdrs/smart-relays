from relays.models import RelayStateChange, Relay


def last_known_relay_state(relay: Relay):
    last_state = RelayStateChange.objects.last_known_state(relay)
    return last_state.new_state if last_state else False


def last_know_relay_state_change_timestamp(relay: Relay):
    last_state = RelayStateChange.objects.last_known_state(relay)
    return last_state.timestamp if last_state else None
