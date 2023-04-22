from django.http import HttpRequest


def set_session_parameter(request: HttpRequest, key: str, value: any):
    request.session[key] = value


def delete_session_parameter(request: HttpRequest, key: str, ignore_missing: bool = True):
    try:
        del request.session[key]
    except KeyError as e:
        if not ignore_missing:
            raise e
