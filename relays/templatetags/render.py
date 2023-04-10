from django import template
from django.utils.safestring import mark_safe
from django.utils.text import Truncator

from accounts.models import User
from relays.models import RelayAuditRecord, RelayUpdateLog, RelayCreateLog, Relay, UserRelayShare

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


@register.inclusion_tag('includes/relay_card.html', takes_context=True)
def render_relay_card(context, relay: Relay):
    return {
        'relay': relay,
        'share': relay.get_share(context.request.user)
    }


@register.simple_tag()
def render_permission_level_progress_bar(relay_share: UserRelayShare):
    def get_color():
        return ('is-danger', 'is-warning', 'is-success')[relay_share.permission_level]
    return mark_safe(
        f'''
         <progress
                class="progress {get_color()}"
                value="{relay_share.permission_level + 1}" max="{len(UserRelayShare.PermissionLevel.values)}"
                title="{relay_share.get_permission_level_display()}"
         ></progress>
        '''
    )
