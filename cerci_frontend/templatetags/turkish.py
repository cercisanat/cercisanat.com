from django import template
from unicode_tr import unicode_tr

register = template.Library()


@register.filter()
def turkish_upper(value):
    return unicode_tr(value).upper()


@register.filter()
def turkish_lower(value):
    return unicode_tr(value).lower()
