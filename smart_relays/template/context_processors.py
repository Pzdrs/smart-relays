from django.http import HttpRequest

from smart_relays.utils.config import get_project_config


def defaults(request: HttpRequest):
    return {
        'defaults': {
            'title': get_project_config().default_title,
        }
    }
