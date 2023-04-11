from accounts.models import User
from relays.models import Relay, UserRelayShare


def user_owns_relay_or_has_full_access(user: User, relay: Relay) -> bool:
    share: UserRelayShare = relay.get_share(user)
    if share is not None:
        return share.is_full_access()
    else:
        return relay.user == user
