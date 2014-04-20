from django.contrib import admin

from .models import Newsletter, Subscriber

admin.site.register(Newsletter)
admin.site.register(Subscriber)
