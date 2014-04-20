from django import template
register = template.Library()
import re


@register.filter(name='youtube_embed_url')
def youtube_embed_url(value):
    value = re.sub(
        r'(https?://(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)(\w*)(&(amp;)?[\w\?=]*)?)',
        r'<iframe width="560" height="315" src="http://www.youtube.com/embed/\2" frameborder="0" allowfullscreen></iframe>',
        value)
    return value

youtube_embed_url.is_safe = True
