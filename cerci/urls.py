from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.http import HttpResponse


urlpatterns = patterns(
    '',
    url(r'', include('cerci_frontend.urls')),
    # url(r'^cerci/', include('cerci.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^newsletters/', include('cerci_newsletters.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include('cerci_admin.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^arama/', include('haystack.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()

if settings.ENVIRONMENT == 'prod':
    urlpatterns += url(
        r'^robots\.txt$',
        lambda r: HttpResponse(
            "User-agent: *\nAllow: /\nDisallow: /admin", mimetype="text/plain")
    ),
else:
    urlpatterns += url(
        r'^robots\.txt$',
        lambda r: HttpResponse(
            "User-agent: *\nDisallow: /", mimetype="text/plain")),
