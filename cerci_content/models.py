from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from categories.models import CategoryBase
from image_cropping import ImageCropField, ImageRatioField
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from taggit_autocomplete.managers import TaggableManager


class Genre(CategoryBase):
    description = models.TextField(
        blank=True, default="", null=True,
        verbose_name=_('Description'))
    spotting_order = models.IntegerField(verbose_name=_('Order'))

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        ordering = ['spotting_order']

Genre._meta.get_field('parent').verbose_name = _("Parent")
Genre._meta.get_field('name').verbose_name = _("Name")
Genre._meta.get_field('slug').verbose_name = _("Slug")
Genre._meta.get_field('active').verbose_name = _("Active")


class Author(models.Model):
    user = models.OneToOneField(
        User, related_name='author',
        null=True, blank=True, verbose_name=_('User'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name=_('Slug'))
    biography = models.TextField(blank=True, verbose_name=_('Biography'))
    image = ImageCropField(upload_to="images/author/",
                           blank=True, verbose_name=_('Image'))
    cropping = ImageRatioField('image', '360x430')
    is_published = models.BooleanField(verbose_name=_('Is Published'),
                                       blank=True)
    created_at = models.DateTimeField(default=now(),
                                      verbose_name=_('Created At'))
    updated_at = models.DateTimeField(verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/yazar/%s" % self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:99]
        self.updated_at = now()
        super(Author, self).save(*args, **kwargs)


def get_illustrations():
    return IssueContent.objects.filter(is_figure=True)


class IssueContent(models.Model):
    tags = TaggableManager(blank=True)
    genres = models.ManyToManyField(Genre, verbose_name=_('Genre'),
                                    null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name=_('Title'),
                             blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name=_('Slug'))
    authors = models.ManyToManyField(Author, verbose_name=_('Author'))
    image = models.ImageField(
        upload_to="images/illustrations/",
        blank=True, verbose_name=_('Image'),
        help_text=_('This image will be used for social sharing sites.'))
    is_figure = models.BooleanField(
        default=False, verbose_name=_('Is this content a figure?'))
    figures = models.ManyToManyField(
        'IssueContent', verbose_name=_('Figures'),
        limit_choices_to={'id__in': get_illustrations},
        null=True, blank=True)
    audios = models.ManyToManyField('Audio', verbose_name=_('Audio'),
                                    null=True, blank=True)
    spot = models.TextField(verbose_name=_('Spot'), blank=True, null=True)
    body = models.TextField(verbose_name=_('Body'), blank=True, null=True)
    is_published = models.BooleanField(verbose_name=_('Is Published'),
                                       blank=True)
    created_at = models.DateTimeField(default=now(),
                                      verbose_name=_('Created At'))
    updated_at = models.DateTimeField(verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Issue Content')
        verbose_name_plural = _('Issue Contents')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if len(self.link_to_issue.all()):
            return "/dergi/%s/%s" % (self.link_to_issue.all()[0].issue.number,
                                     self.slug)
        return "/"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:99]
        self.updated_at = now()
        super(IssueContent, self).save(*args, **kwargs)

    def next_prev(self, issue, direction):
        i2c = issue.issue2content_set.all()
        order = i2c.get(content=self).order
        if direction == 'next':
            orders_gt_self = i2c.filter(order__gt=order).order_by('order')
            if orders_gt_self.count():
                return orders_gt_self[0].content
        elif direction == 'prev':
            orders_lt_self = i2c.filter(order__lt=order).order_by('-order')
            if orders_lt_self.count():
                return orders_lt_self[0].content

    def next(self, issue):
        return self.next_prev(issue, 'next')

    def prev(self, issue):
        return self.next_prev(issue, 'prev')

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)


class GalleryImage(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True,
                             verbose_name=_('Title'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('Description'))
    image = models.ImageField(upload_to="images/gallery/", blank=True,
                              verbose_name=_('Image'),
                              help_text=_('Gallery Image'))

    class Meta:
        verbose_name = _('Gallery Image')
        verbose_name_plural = _('Gallery Images')


class Gallery(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True,
                             verbose_name=_('Title'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('Description'))
    images = models.ManyToManyField(GalleryImage, through=('Gallery2Image'),
                                    verbose_name=_('Images'))

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')

    def __unicode__(self):
        return 'Gallery (id=%s)' % self.id


class Gallery2Image(models.Model):
    gallery = models.ForeignKey(Gallery, verbose_name=_('Gallery'))
    image = models.ForeignKey(GalleryImage, verbose_name=_('GalleryImage'))
    order = models.IntegerField(verbose_name=_('Order'), null=True, default=0)

    def __unicode__(self):
        return '%s (%s) -> %s, order: %s' % (
            self.gallery.title, self.gallery.pk,
            self.image.image.url, self.order)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ['order']
        unique_together = ('gallery', 'image',)


class Audio(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name=_('Slug'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('Description'))
    audio = models.FileField(upload_to="audio/", verbose_name=_('Audio'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:99]
        super(Audio, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Audio')
        verbose_name_plural = _('Audios')
