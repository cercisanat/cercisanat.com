from django import template
from django.template import Context
from django.template.loader import get_template
register = template.Library()
import re

from cerci_content.models import Gallery


@register.filter(name='gallery_embed')
def gallery_embed(value):
    matches = re.findall('\[gallery:(.*)\]', value)
    galleries = Gallery.objects.filter(slug__in=matches)

    for gallery in galleries:
        context = Context({'gallery': gallery})
        html = get_template(
            'gallery/%s.html' % gallery.display_with).render(context)
        value = value.replace('[gallery:%s]' % gallery.slug, html)
    return value

gallery_embed.is_safe = True
