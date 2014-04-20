from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^cerci_issue/issue/publish/(?P<issue_id>[0-9]+)$',
        'cerci_admin.views.publish_issue', name='publish_issue'),
    url(r'^cerci_issue/issue/unpublish/(?P<issue_id>[0-9]+)$',
        'cerci_admin.views.unpublish_issue', name='unpublish_issue'),
    url(r'^cerci_content/issuecontent/thumbnail/(?P<id>[0-9]+)$',
        'cerci_admin.views.thumbnail_by_id', name='thumbnail_by_id')
)
