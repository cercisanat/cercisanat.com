from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^$', 'cerci_frontend.views.home', name='home'),
    url(r'^(?P<year>[0-9]+)$', 'cerci_frontend.views.home', name='home_year'),
    url(r'^dergi/(?P<issue_number>[-\w]+)$',
        'cerci_frontend.views.current_issue', name='current_issue'),
    url(r'^dergi/(?P<issue_number>[-\w]+)/(?P<contentslug>[-\w]+)$',
        'cerci_frontend.views.current_issuecontent',
        name='current_issuecontent'),
    url(r'^yazar/$', 'cerci_frontend.views.author_list', name='author_list'),
    url(r'^yazar/(?P<author_slug>[-\w]+)$',
        'cerci_frontend.views.author', name='author'),
    url(r'^tur/(?P<genreslug>[-\w]+)$',
        'cerci_frontend.views.genre', name='genre'),
    url(r'^etiket/(?P<tagslug>[-\w]+)$',
        'cerci_frontend.views.tag', name='tag'),
    url(r'^blog/$',
        'cerci_frontend.views.blog', name='blog'),
    url(r'^ekip/$',
        TemplateView.as_view(template_name="crew.html"), name='crew'),
    url(r'^manifesto/$',
        TemplateView.as_view(template_name="manifest.html"), name='manifest'),
    url(r'^takip-et/$',
        TemplateView.as_view(template_name="follow.html"), name='follow'),
    url(r'^yazi-gonder/$',
        TemplateView.as_view(template_name="sendus.html"), name='sendus'),
    url(r'^site-kurallari/$',
        TemplateView.as_view(template_name="rules.html"), name='rules'),
    url(r'^iletisim/$',
        TemplateView.as_view(template_name="contact.html"), name='contact'),
    url(r'^8e434d966ffc\.html/$',
        'cerci_frontend.views.yandex_proof', name="yandex_proof"),
)
