from cerci_content.models import Genre
from django.conf import settings


def genres(request):
    genres = Genre.objects.filter(active=True)
    return {'genres': genres}


def site(request):
    return {'SITE_URL': settings.SITE_URL}


def yandex_metrica_id(request):
    return {'YANDEX_METRICA_ID': getattr(settings, 'YANDEX_METRICA_ID', None)}
