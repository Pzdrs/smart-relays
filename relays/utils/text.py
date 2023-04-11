from django.utils.text import Truncator


def truncate_string(value: str, length: int) -> str:
    return Truncator(value).chars(length)


def value_or_default(value: any, default_value: any) -> any:
    return value or default_value


def translate_bool(value: bool, true: str = 'Yes', false: str = 'No') -> str:
    return true if value else false
