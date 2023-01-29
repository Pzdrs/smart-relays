from django.apps import apps

from api.apps import ApiConfig
from relays.apps import RelaysConfig
from smart_relays.apps import SmartRelaysConfig


def get_project_config() -> SmartRelaysConfig:
    return apps.get_app_config('smart_relays')


def get_api_config() -> ApiConfig:
    return apps.get_app_config('api')


def get_relays_config() -> RelaysConfig:
    return apps.get_app_config('relays')
