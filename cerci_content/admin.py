from cerci_content.models import (Author, IssueContent, Genre, Gallery,
                                  GalleryImage, Gallery2Image, Audio)
from cerci_issue.models import Issue2Content
from django.contrib import admin
import reversion
from image_cropping import ImageCroppingMixin
from django.utils.translation import ugettext as _
from django.core import urlresolvers
from cerci_content.forms import IssueContentAdminModelForm


class Issue2ContentInline(admin.StackedInline):
    model = Issue2Content
    extra = 0
    fields = ('issue', 'is_subject', 'order')
    raw_id_fields = ('issue', 'content')
    # sortable_field_name = "order"
    verbose_name = _('Issue')
    verbose_name_plural = _('Issues')
    autocomplete_lookup_fields = {
        'fk': ['issue'],
    }


class AudioInline(admin.TabularInline):
    model = IssueContent.audios.through
    extra = 0
    readonly_fields = ['slug']

    def slug(self, instance):
        return '[audio:%s]' % instance.audio.slug
    slug.short_description = 'Copy this'


class IssueContentAdmin(reversion.VersionAdmin):

    class Media:
        css = {"all": ('/static/select2/select2.css',
                       '/static/css/select2-fix.css')}
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js',
            '/static/select2/select2.js',
            '/static/js/select.js')

    history_latest_first = True
    ignore_duplicate_revisions = True
    form = IssueContentAdminModelForm
    search_fields = ['title']
    list_display = ('title', 'get_authors_list', 'get_issues_list',
                    'is_published', 'is_figure', 'created_at', 'updated_at')
    list_filter = ('is_published', 'link_to_issue__issue',
                   'authors', 'is_figure', 'genres')
    prepopulated_fields = {'slug': ('title',), }
    readonly_fields = ("created_at", "updated_at", "is_published")
    inlines = (Issue2ContentInline, AudioInline)

    exclude = ('audios',)

    def get_authors_list(self, obj):
        authors = '<ul>'
        for author in obj.authors.all():
            change_url = urlresolvers.reverse(
                'admin:cerci_content_author_change', args=(author.id,))
            authors += '<li><a href="%s">%s</a></li>' % (change_url,
                                                         author.name)
        return authors + '</ul>'
    get_authors_list.short_description = _('Author')
    get_authors_list.allow_tags = True

    def get_issues_list(self, obj):
        issues = '<ul>'
        if obj.is_figure:
            issue_list = []
            issuecontents = obj.issuecontent_set.all()
            for content in issuecontents:
                for issue in content.link_to_issue.all():
                    issue_list.append([issue, 'figure: '])
        else:
            issue_list = [[i, ''] for i in obj.link_to_issue.all()]
        for issue in issue_list:
            change_url = urlresolvers.reverse('admin:cerci_issue_issue_change',
                                              args=(issue[0].issue.id,))
            issues += '<li><a href="%s">%s%s</a></li>' % (
                change_url, issue[1], issue[0].issue.subject)
        return issues + '</ul>'
    get_issues_list.short_description = _('Issue')
    get_issues_list.allow_tags = True


admin.site.register(IssueContent, IssueContentAdmin)


class AuthorAdmin(ImageCroppingMixin, admin.ModelAdmin):
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',), }
    readonly_fields = ("created_at", "updated_at",)
    list_display = ('name', 'is_published', 'created_at', 'updated_at')
    list_filter = ('is_published', 'created_at', 'updated_at')

admin.site.register(Author, AuthorAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'spotting_order')
    exclude = ('parent',)
    prepopulated_fields = {'slug': ('name',), }

admin.site.register(Genre, GenreAdmin)


class Gallery2ImageInline(admin.TabularInline):
    model = Gallery2Image
    extra = 0
    fields = ('image', 'order')
    sortable_field_name = 'order'


class GalleryAdmin(admin.ModelAdmin):
    inlines = (Gallery2ImageInline,)
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Gallery, GalleryAdmin)


class GalleryImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(GalleryImage, GalleryImageAdmin)


class AudioAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Audio, AudioAdmin)
