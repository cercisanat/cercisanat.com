from django.core.management.base import BaseCommand
from utils.cache import destroy_cache


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        destroy_cache()
        self.stdout.write('Cleared cache\n')
