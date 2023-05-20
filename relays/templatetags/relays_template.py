from django import template
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe

from relays.models import RelayAuditRecord, Relay, UserRelayShare, Channel
from relays.utils.dates import format_date
from relays.utils.template import get_progress_bar_color

register = template.Library()


@register.simple_tag
def render_audit_log(log: RelayAuditRecord, include_relay: bool = False):
    return mark_safe(f'''
        <tr>
            <td>{format_date(log.timestamp)}</td>
            {f'<td>{log.relay}</td>' if include_relay else ''}
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


@register.inclusion_tag('includes/pagination/pagination_range.html')
def render_pagination_range(
        paginator: Paginator,
        page: int,
        one_each_side: int = 1,
        on_ends: int = 1,
        range_ellipsis: any = None
):
    page_range = paginator.get_elided_page_range(page, on_each_side=one_each_side, on_ends=on_ends)
    return {
        'page_range': [int(page) if str(page).isnumeric() else None for page in page_range],
        'current_page': page,
        'ellipsis': range_ellipsis if range_ellipsis else paginator.ELLIPSIS
    }


@register.inclusion_tag('includes/slot_status.html')
def slot_status():
    slots_max = Channel.objects.count()
    slots_used = Channel.objects.in_use().count()
    return {
        'slots_used': slots_used,
        'slots_max': slots_max,
        'slots_left': slots_max - slots_used,
        'progress_color': get_progress_bar_color(slots_used / slots_max) if slots_max > 0 else ''
    }
