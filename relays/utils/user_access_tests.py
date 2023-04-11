from accounts.models import User
from relays.models import Relay, UserRelayShare


def owner(user: User, relay: Relay) -> bool:
    return relay.user == user


def full_access(user: User, relay: Relay) -> bool:
    share: UserRelayShare = relay.get_share(user)
    return share is not None and share.is_full_access()


def control(user: User, relay: Relay) -> bool:
    share: UserRelayShare = relay.get_share(user)
    return share is not None and share.is_control()


def at_least_control(user: User, relay: Relay) -> bool:
    share: UserRelayShare = relay.get_share(user)
    return share is not None and (share.is_control() or share.is_full_access())


def owner_or_full_access(user: User, relay: Relay) -> bool:
    return owner(user, relay) or full_access(user, relay)


def owner_or_at_least_control(user: User, relay: Relay) -> bool:
    return owner(user, relay) or at_least_control(user, relay)
