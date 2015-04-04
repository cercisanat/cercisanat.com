# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(unique=True, verbose_name='Say\u0131')),
                ('subject', models.CharField(max_length=255, verbose_name='Dosya Konusu')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='URL Uyumlu')),
                ('editorial_title', models.CharField(max_length=255, verbose_name='Edit\xf6rden Ba\u015fl\u0131\u011f\u0131', blank=True)),
                ('editorial', models.TextField(verbose_name='Edit\xf6rden', blank=True)),
                ('copyright_page', models.TextField(verbose_name='K\xfcnye')),
                ('cover', models.ImageField(upload_to=b'images/issue/', verbose_name='Kapak')),
                ('is_published', models.BooleanField(default=False, verbose_name='Yay\u0131nda m\u0131')),
                ('published_at', models.DateField(null=True, verbose_name='Yay\u0131n Tarihi', blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 20, 3, 58, 624394, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi')),
                ('updated_at', models.DateTimeField(verbose_name='G\xfcncelleme Tarihi')),
            ],
            options={
                'get_latest_by': 'published_at',
                'verbose_name': 'Dergi',
                'verbose_name_plural': 'Dergiler',
            },
        ),
        migrations.CreateModel(
            name='Issue2Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0, null=True, verbose_name='S\u0131ra')),
                ('is_subject', models.BooleanField(verbose_name='Dosya Konusu mu')),
                ('content', models.ForeignKey(related_name='link_to_issue', verbose_name='\u0130\xe7erik', to='cerci_content.IssueContent')),
                ('issue', models.ForeignKey(verbose_name='Dergi', to='cerci_issue.Issue')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u0130\xe7erik',
                'verbose_name_plural': '\u0130\xe7erikler',
            },
        ),
        migrations.CreateModel(
            name='IssueFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issue_file', models.FileField(upload_to=b'files/issue/', verbose_name='Dosya')),
                ('format', models.CharField(default=b'ePub3', max_length=16, verbose_name='Bi\xe7im', choices=[(b'ePub3', b'ePub3'), (b'PDF', b'PDF')])),
                ('issue', models.ForeignKey(verbose_name='Dergi', to='cerci_issue.Issue')),
            ],
            options={
                'verbose_name': 'Dosya',
                'verbose_name_plural': 'Dosyalar',
            },
        ),
        migrations.AddField(
            model_name='issue',
            name='contents',
            field=models.ManyToManyField(to='cerci_content.IssueContent', verbose_name='\u0130\xe7erikler', through='cerci_issue.Issue2Content'),
        ),
        migrations.AddField(
            model_name='issue',
            name='cover_design',
            field=models.ManyToManyField(to='cerci_content.Author', null=True, verbose_name='Kapak Tasar\u0131m\u0131'),
        ),
        migrations.AlterUniqueTogether(
            name='issue2content',
            unique_together=set([('issue', 'content')]),
        ),
    ]
