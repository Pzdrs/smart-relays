from accounts.models import User
from relays.models import Relay, UserRelayShare


def owner(user: User, relay: Relay) -> bool:
    """
    Requires the user to be the owner of the relay.
    """
    return relay.user == user


def full_access(user: User, relay: Relay) -> bool:
    """
    Requires the relay to be shared with the user (full access).
    """
    share: UserRelayShare = relay.get_share(user)
    return share is not None and share.is_full_access()


def control(user: User, relay: Relay) -> bool:
    """
    Requires the relay to be shared with the user (control).
    """
    share: UserRelayShare = relay.get_share(user)
    return share is not None and share.is_control()


def at_least_control(user: User, relay: Relay) -> bool:
    """
    Requires the relay to be shared with the user (control or full access).
    """
    share: UserRelayShare = relay.get_share(user)
    return share is not None and (share.is_control() or share.is_full_access())


def owner_or_full_access(user: User, relay: Relay) -> bool:
    """
    Requires the user to be the owner of the relay or the relay needs to be shared with the user (full access).
    """
    return owner(user, relay) or full_access(user, relay)


def owner_or_at_least_control(user: User, relay: Relay) -> bool:
    """
    Requires the user to be the owner of the relay or the relay needs to be shared with
    the user (control or full access).
    """
    return owner(user, relay) or at_least_control(user, relay)


def owner_or_shared(user: User, relay: Relay) -> bool:
    """
    Requires the user to be the owner of the relay or the relay needs to be shared with the user (any permission level).
    """
    return owner(user, relay) or relay.get_share(user) is not None


def superuser(user: User) -> bool:
    """
    Requires the user to be a superuser.
    """
    return user.is_superuser


def owner_or_full_access_or_superuser(user: User, relay: Relay) -> bool:
    """
    Requires the user to be the owner of the relay or the relay needs to be shared with the user (full access) or the
    user needs to be a superuser.
    """
    return owner(user, relay) or full_access(user, relay) or superuser(user)


def owner_or_shared_or_superuser(user: User, relay: Relay) -> bool:
    """
    Requires the user to be the owner of the relay or the relay needs to be shared with the user (any permission level)
    or the user needs to be a superuser.
    """
    return owner(user, relay) or relay.get_share(user) is not None or superuser(user)
