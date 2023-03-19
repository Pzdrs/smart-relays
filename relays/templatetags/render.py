from django import template
from django.utils.safestring import mark_safe
from django.utils.text import Truncator

from relays.models import RelayAuditRecord, RelayUpdateLog, RelayCreateLog

register = template.Library()


def change_in_value(old, new):
    return f'''
        <i>{default(truncate(old, 25), "Blank")}</i>
        <i class="fa-solid fa-arrow-right px-1"></i>
        <i>{truncate(new, 25)}</i>
    '''


def truncate(value, length):
    return Truncator(value).chars(length)


def default(value, default_value):
    return value or default_value


def format_date(date):
    return date.strftime('%d/%m/%Y %H:%M:%S')


@register.simple_tag
def render_audit_log(log: RelayAuditRecord):
    if isinstance(log, RelayUpdateLog):
        return mark_safe(
            f'''
            <tr>
                <td>{format_date(log.timestamp)}</td>
                <td>{log.user if log.user else '-'}</td>
                <td>
                    The <b>{log.field}</b> field changed - {change_in_value(log.old_value, log.new_value)}
                </td>
            </tr>
            '''
        )
    elif isinstance(log, RelayCreateLog):
        return mark_safe(
            f'''
            <tr>
                <td>{format_date(log.timestamp)}</td>
                <td>{log.user if log.user else '-'}</td>
                <td>Created new relay - <i>{log.relay}</i></td>
            </tr>
            '''
        )
