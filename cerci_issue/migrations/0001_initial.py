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
                ('number', models.IntegerField(unique=True, verbose_name='Number')),
                ('subject', models.CharField(max_length=255, verbose_name='Issue Subject')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('editorial_title', models.CharField(max_length=255, verbose_name='Editorial Title', blank=True)),
                ('editorial', models.TextField(verbose_name='Editorial', blank=True)),
                ('copyright_page', models.TextField(verbose_name='Copyright Page')),
                ('cover', models.ImageField(upload_to=b'images/issue/', verbose_name='Cover')),
                ('is_published', models.BooleanField(verbose_name='Is Published')),
                ('published_at', models.DateField(null=True, verbose_name='Published At', blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 7, 38, 20, 329079, tzinfo=utc), verbose_name='Created At')),
                ('updated_at', models.DateTimeField(verbose_name='Updated At')),
            ],
            options={
                'get_latest_by': 'published_at',
                'verbose_name': 'Issue',
                'verbose_name_plural': 'Issues',
            },
        ),
        migrations.CreateModel(
            name='Issue2Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0, null=True, verbose_name='S\u0131ralama')),
                ('is_subject', models.BooleanField(verbose_name='Is Subject')),
                ('content', models.ForeignKey(related_name='link_to_issue', verbose_name='Content', to='cerci_content.IssueContent')),
                ('issue', models.ForeignKey(verbose_name='Issue', to='cerci_issue.Issue')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Content',
                'verbose_name_plural': 'Contents',
            },
        ),
        migrations.CreateModel(
            name='IssueFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issue_file', models.FileField(upload_to=b'files/issue/', verbose_name='Dosya')),
                ('format', models.CharField(default=b'ePub3', max_length=16, verbose_name='Format', choices=[(b'ePub3', b'ePub3'), (b'PDF', b'PDF')])),
                ('issue', models.ForeignKey(verbose_name='Issue', to='cerci_issue.Issue')),
            ],
            options={
                'verbose_name': 'Dosya',
                'verbose_name_plural': 'Files',
            },
        ),
        migrations.AddField(
            model_name='issue',
            name='contents',
            field=models.ManyToManyField(to='cerci_content.IssueContent', verbose_name='Contents', through='cerci_issue.Issue2Content'),
        ),
        migrations.AddField(
            model_name='issue',
            name='cover_design',
            field=models.ManyToManyField(to='cerci_content.Author', null=True, verbose_name='Cover Design'),
        ),
        migrations.AlterUniqueTogether(
            name='issue2content',
            unique_together=set([('issue', 'content')]),
        ),
    ]
