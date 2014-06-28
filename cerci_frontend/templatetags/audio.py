from django import template
register = template.Library()
import re

from cerci_content.models import Audio


@register.filter(name='audio_embed')
def audio_embed(value):
    matches = re.findall('\[audio:(.*)\]', value)
    audios = Audio.objects.filter(slug__in=matches)

    for audio in audios:
        value = value.replace(
            '[audio:%s]' % audio.slug,
            """
            <div class="audio">
            <strong>%s</strong><br/>
            <div class="pull-left">
            <audio controls="controls" preload="none">
                <source src="%s" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            </div>
            <div class="pull-left audio-description">
            %s
            </div>
            <div class="clearfix"></div>
            </div>
            """ % (audio.title, audio.audio.url, audio.description))
    return value

audio_embed.is_safe = True
