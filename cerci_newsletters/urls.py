from django.conf.urls import patterns, url

from .views import SubscribeFormView, UnsubscribeView


urlpatterns = patterns(
    '',
    url(r'^$', SubscribeFormView.as_view(), name='subscribe_form'),
    url(r'^unsubscribe/$', UnsubscribeView.as_view(), name='unsubscribe')
)
