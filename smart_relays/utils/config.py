from django.apps import apps, AppConfig

from accounts.apps import AccountsConfig
from api.apps import ApiConfig
from relays.apps import RelaysConfig
from smart_relays.apps import SmartRelaysConfig


def get_config(app: str):
    return apps.get_app_config(app)


def get_project_config() -> SmartRelaysConfig:
    return get_config('smart_relays')


def get_api_config() -> ApiConfig:
    return get_config('api')


def get_relays_config() -> RelaysConfig:
    return get_config('relays')


def get_accounts_config() -> AccountsConfig:
    return get_config('accounts')
