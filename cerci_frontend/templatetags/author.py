from django import template
from django.core.urlresolvers import reverse
import os
register = template.Library()


@register.filter(is_safe=True)
def author_list(authors):
    author_str = ''
    for author in authors:
        if author.is_published:
            url = reverse('author', args=(author.slug, ))
            author_str += '<a href="' + url + '">' + author.name + '</a>, '
        else:
            author_str += author.name + ', '
    return author_str[:-2]


@register.filter(is_safe=True)
def author_list_plain(authors):
    author_str = ''
    for author in authors:
        author_str += author.name + ', '
    return author_str[:-2]


@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.filter
def remove_media(value):
    return value.replace('/media/', '').replace(' ', '')
