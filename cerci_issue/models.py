from django.db import models
from cerci_content.models import IssueContent, Author
from datetime import datetime
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.utils.timezone import now


def get_unused_contents():
    return IssueContent.objects.filter(issue=None)


class Issue(models.Model):
    number = models.IntegerField(unique=True, verbose_name=_('Number'))
    subject = models.CharField(max_length=255, verbose_name=_('Issue Subject'))
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_('Slug'))
    editorial_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Editorial Title'))
    editorial = models.TextField(blank=True, verbose_name=_('Editorial'))
    copyright_page = models.TextField(verbose_name=_('Copyright Page'))
    cover = models.ImageField(
        upload_to="images/issue/",
        verbose_name=_('Cover'))
    cover_design = models.ManyToManyField(
        Author, verbose_name=_('Cover Design'), null=True)
    contents = models.ManyToManyField(
        IssueContent, through="Issue2Content",
        limit_choices_to={"issue": "self"},
        verbose_name=_('Contents'))
    is_published = models.BooleanField(
        blank=True, default=False,
        verbose_name=_('Is Published'))
    published_at = models.DateField(
        null=True, blank=True, verbose_name=_('Published At'))
    created_at = models.DateTimeField(
        default=now(), verbose_name=_('Created At'))
    updated_at = models.DateTimeField(verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Issue')
        verbose_name_plural = _('Issues')
        get_latest_by = 'published_at'

    def get_absolute_url(self):
        return "/dergi/%s" % self.number

    def __unicode__(self):
        return self.subject

    def get_contents(self):
        return self.issue2content_set.prefetch_related(
            'content', 'content__authors', 'content__genres'
        ).filter(content__is_published=True)

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = datetime.now()

        if not self.slug:
            self.slug = slugify(self.subject)[:99]
        self.updated_at = now()
        super(Issue, self).save(*args, **kwargs)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "subject__icontains",)


class Issue2Content(models.Model):
    issue = models.ForeignKey(Issue, verbose_name=_('Issue'))
    content = models.ForeignKey(
        IssueContent, related_name='link_to_issue',
        verbose_name=_('Content'))
    order = models.IntegerField(verbose_name=_('Order'), null=True, default=0)
    is_subject = models.BooleanField(verbose_name=_('Is Subject'), blank=True)

    def __unicode__(self):
        return '%s (%s %s) -> %s, order: %s' % (
            self.issue.subject, _('Number'), self.issue.number,
            self.content.title, self.order)

    class Meta:
        verbose_name = _('Content')
        verbose_name_plural = _('Contents')
        ordering = ['order']
        unique_together = ('issue', 'content', )


class IssueFile(models.Model):
    FORMATS = (('ePub3', 'ePub3'),
               ('PDF', 'PDF'))

    EXTENSIONS = {'ePub3': 'epub',
                  'PDF': 'pdf'}

    issue = models.ForeignKey(Issue, verbose_name=_('Issue'))
    issue_file = models.FileField(
        upload_to="files/issue/", verbose_name=_('File'))
    format = models.CharField(
        max_length=16, verbose_name=_('Format'),
        choices=FORMATS, default="ePub3")

    def __unicode__(self):
        return "%(issue)s -> %(format)s" % {'issue': self.issue.slug,
                                            'format': self.format}

    def get_filename(self):
        return "cerci-sayi-%(number)s.%(format)s" % {
            'number': self.issue.number,
            'format': self.EXTENSIONS[self.format]}

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')
