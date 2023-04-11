import datetime


def format_date(date: datetime) -> str:
    return date.strftime('%d/%m/%Y %H:%M:%S')
