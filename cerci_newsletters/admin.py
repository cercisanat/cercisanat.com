from django.contrib import admin

from .models import Newsletter, Subscriber, UnsubscribeToken

admin.site.register(Newsletter)
admin.site.register(Subscriber)
admin.site.register(UnsubscribeToken)
