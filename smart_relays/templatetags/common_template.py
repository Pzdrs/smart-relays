from django.forms import Form, ChoiceField
from django.template.defaulttags import register
from django.utils.safestring import mark_safe


@register.filter
def time_delta_nice(date_time):
    from datetime import datetime, timedelta
    now = datetime.now(tz=date_time.tzinfo)
    delta = now - date_time
    if delta < timedelta(seconds=60):
        return f'{delta.seconds} seconds ago'
    elif delta < timedelta(minutes=60):
        return f'{delta.seconds // 60} minutes ago'
    elif delta < timedelta(hours=24):
        return f'{delta.seconds // 3600} hours ago'
    elif delta < timedelta(days=7):
        return f'{delta.days} days ago'
    elif delta < timedelta(weeks=4):
        return f'{delta.days // 7} weeks ago'
    elif delta < timedelta(days=365):
        return f'{delta.days // 30} months ago'
    else:
        return f'{delta.days // 365} years ago'


@register.inclusion_tag('includes/form.html')
def render_form(form: Form, field_wrap: bool = True, label: bool = True):
    return {
        'form': form,
        'field_wrap': field_wrap,
        'label': label
    }


@register.simple_tag()
def render_form_field(field):
    if isinstance(field.field, ChoiceField) and field.widget_type != 'hidden':
        return mark_safe(f'<div class="select">{field}</div>')
    else:
        return mark_safe(field)
