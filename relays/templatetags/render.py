from django import template
from django.utils.safestring import mark_safe

from relays.models import RelayAuditRecord, Relay, UserRelayShare
from relays.utils.dates import format_date

register = template.Library()


@register.simple_tag
def render_audit_log(log: RelayAuditRecord, global_record: bool = False):
    return mark_safe(f'''
        <tr>
            <td>{format_date(log.timestamp)}</td>
            {f'<td>{log.relay}</td>' if global_record else ''}
            <td>{log.user if log.user else '-'}</td>
            <td>{log.get_display()}</td>
        </tr>
    ''')


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
