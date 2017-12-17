from django import template
from .. import app_reverse

register = template.Library()

@register.simple_tag(takes_context=False)
def app_url(view_name, *args, **kwargs):
    return app_reverse(view_name, args=args, kwargs=kwargs)

