from django.conf.urls import patterns, url

from .views import SubscribeFormView


urlpatterns = patterns(
    '',
    url(r'^$', SubscribeFormView.as_view(), name='subscribe_form')
)
