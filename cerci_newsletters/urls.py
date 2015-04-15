from django.conf.urls import patterns, url

from .views import SubscribeFormView, UnsubscribeView


urlpatterns = patterns(
    '',
    url(r'^$', SubscribeFormView.as_view(), name='subscribe_form'),
    url(r'^unsubscribe/$', UnsubscribeView.as_view(), name='unsubscribe'),
    url(r'^send/(?P<issue_number>[-\w]+)$', 'cerci_newsletters.views.send',
        name='send_newsletters'),
    url(r'^send/(?P<issue_number>[-\w]+)/test$',
        'cerci_newsletters.views.test_sending',
        name='send_newsletters_test'),
    url(r'^email-template-debug/(?P<issue_number>[-\w]+)$',
        'cerci_newsletters.views.email_template_debug',
        name='email_template_debug')
)
