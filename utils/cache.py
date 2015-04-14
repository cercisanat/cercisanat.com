import os
import shutil
from django.conf import settings


def destroy_cache():
    path = settings.CACHES['default']['LOCATION']
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
