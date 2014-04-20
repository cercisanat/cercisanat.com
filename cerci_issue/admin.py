from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext as _

from ckeditor.widgets import CKEditorWidget

from cerci_issue.models import Issue, Issue2Content, IssueFile


class Issue2ContentInline(admin.TabularInline):
    model = Issue2Content
    extra = 1
    fields = ('content', 'order', 'is_subject')
    sortable_field_name = "order"
    raw_id_fields = ('content',)
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'fk': ['content'],
    }


class IssueFileInline(admin.TabularInline):
    model = IssueFile
    extra = 1
    fields = ('issue_file', 'format')
    raw_id_fields = ('issue',)


class IssueAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ('/static/select2/select2.css',
                       '/static/css/select2-fix.css')}
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js',
            '/static/select2/select2.js',
            '/static/js/select.js')

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
    inlines = (Issue2ContentInline, IssueFileInline)
    list_display = ('subject', 'number', 'is_published', 'get_published_at')
    prepopulated_fields = {'slug': ('subject',), }
    readonly_fields = ("created_at", "updated_at", "is_published")

    def get_published_at(self, obj):
        if obj.published_at:
            return obj.published_at.strftime("%B %Y")
        return 'X'
    get_published_at.short_description = _('Published At')

admin.site.register(Issue, IssueAdmin)
