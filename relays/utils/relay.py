from accounts.models import User
from relays.models import Relay, UserRelayPermission
from smart_relays.utils.config import get_project_config


def relay_slots_breakdown() -> tuple[int, int, int]:
    max_relays = get_project_config().max_relays
    current_relays = Relay.objects.count()
    return max_relays, current_relays, max_relays - current_relays


def user_all_access_test(user: User, relay: Relay):
    permission: UserRelayPermission = relay.get_permission(user)
    return not permission or permission.permission_level in (UserRelayPermission.PermissionLevel.ALL_ACCESS,)
