# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import mptt.fields
from django.utils.timezone import utc
from django.conf import settings
import image_cropping.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Ba\u015fl\u0131k')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='URL Uyumlu')),
                ('description', models.TextField(null=True, verbose_name='A\xe7\u0131klama', blank=True)),
                ('audio', models.FileField(upload_to=b'audio/', verbose_name='Audio')),
            ],
            options={
                'verbose_name': 'Audio',
                'verbose_name_plural': 'Audios',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u0130sim')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='URL Uyumlu')),
                ('biography', models.TextField(verbose_name='\xd6zge\xe7mi\u015f', blank=True)),
                ('image', image_cropping.fields.ImageCropField(upload_to=b'images/author/', verbose_name='G\xf6rsel', blank=True)),
                (b'cropping', image_cropping.fields.ImageRatioField(b'image', '360x430', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping')),
                ('is_published', models.BooleanField(verbose_name='Yay\u0131nda m\u0131')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 20, 3, 58, 610497, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi')),
                ('updated_at', models.DateTimeField(verbose_name='G\xfcncelleme Tarihi')),
                ('user', models.OneToOneField(related_name='author', null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Kullan\u0131c\u0131')),
            ],
            options={
                'verbose_name': 'Yazar',
                'verbose_name_plural': 'Yazarlar',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Ba\u015fl\u0131k', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='URL Uyumlu')),
                ('description', models.TextField(null=True, verbose_name='A\xe7\u0131klama', blank=True)),
                ('display_with', models.CharField(default=b'bootstrap_carousel', max_length=20, verbose_name='Display With', choices=[(b'bootstrap_carousel', 'Inline Gallery'), (b'photobox_gallery', 'Overlay')])),
            ],
            options={
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Galleries',
            },
        ),
        migrations.CreateModel(
            name='Gallery2Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0, null=True, verbose_name='S\u0131ra')),
                ('gallery', models.ForeignKey(verbose_name='Gallery', to='cerci_content.Gallery')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'G\xf6rsel',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Ba\u015fl\u0131k', blank=True)),
                ('description', models.TextField(null=True, verbose_name='A\xe7\u0131klama', blank=True)),
                ('image', models.ImageField(help_text='Gallery Image', upload_to=b'images/gallery/', verbose_name='G\xf6rsel', blank=True)),
            ],
            options={
                'verbose_name': 'Gallery Image',
                'verbose_name_plural': 'Gallery Images',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='ad\u0131')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('active', models.BooleanField(default=True, verbose_name='etkin')),
                ('description', models.TextField(default=b'', null=True, verbose_name='A\xe7\u0131klama', blank=True)),
                ('spotting_order', models.IntegerField(verbose_name='S\u0131ra')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='parent', blank=True, to='cerci_content.Genre', null=True)),
            ],
            options={
                'ordering': ['spotting_order'],
                'verbose_name': 'T\xfcr',
                'verbose_name_plural': 'T\xfcrler',
            },
        ),
        migrations.CreateModel(
            name='IssueContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Ba\u015fl\u0131k', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='URL Uyumlu')),
                ('image', models.ImageField(help_text='This image will be used for social sharing sites.', upload_to=b'images/illustrations/', verbose_name='G\xf6rsel', blank=True)),
                ('is_figure', models.BooleanField(default=False, verbose_name='Bu i\xe7erik bir fig\xfcr m\xfc?')),
                ('spot', models.TextField(null=True, verbose_name='Spot', blank=True)),
                ('body', models.TextField(null=True, verbose_name='Metin', blank=True)),
                ('is_published', models.BooleanField(verbose_name='Yay\u0131nda m\u0131')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 20, 3, 58, 612319, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi')),
                ('updated_at', models.DateTimeField(verbose_name='G\xfcncelleme Tarihi')),
                ('audios', models.ManyToManyField(to='cerci_content.Audio', null=True, verbose_name='Audio', blank=True)),
                ('authors', models.ManyToManyField(to='cerci_content.Author', verbose_name='Yazar')),
                ('figures', models.ManyToManyField(to='cerci_content.IssueContent', null=True, verbose_name='Fig\xfcrler', blank=True)),
                ('genres', models.ManyToManyField(to='cerci_content.Genre', null=True, verbose_name='T\xfcr', blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Dergi \u0130\xe7eri\u011fi',
                'verbose_name_plural': 'Dergi \u0130\xe7erikleri',
            },
        ),
        migrations.AddField(
            model_name='gallery2image',
            name='image',
            field=models.ForeignKey(verbose_name='GalleryImage', to='cerci_content.GalleryImage'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='images',
            field=models.ManyToManyField(to='cerci_content.GalleryImage', verbose_name='Images', through='cerci_content.Gallery2Image'),
        ),
        migrations.AlterUniqueTogether(
            name='gallery2image',
            unique_together=set([('gallery', 'image')]),
        ),
    ]
