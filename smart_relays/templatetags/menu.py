from django import template
from django.utils.safestring import mark_safe

from smart_relays.utils.menu import MenuItem, Label, Link

register = template.Library()


@register.simple_tag()
def render_menu(menu: tuple[MenuItem]):
    html = ''
    for i, item in enumerate(menu):
        prev = menu[i - 1] if i > 0 else None
        if isinstance(item, Link) and isinstance(prev, Label):
            html += f'<ul class="menu-list">\n'
        if isinstance(item, Label) and isinstance(prev, Link):
            html += '</ul>\n'
        html += item.html()
    return mark_safe(html)
