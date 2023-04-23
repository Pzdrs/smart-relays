from django.http import HttpRequest

from accounts.models import User


def superuser(request: HttpRequest):
    return request.user.is_superuser


def same_user(request: HttpRequest, user: User):
    return request.user.pk == user.pk


def same_user_or_superuser(request: HttpRequest, user: User):
    return same_user(request, user) or superuser(request)
