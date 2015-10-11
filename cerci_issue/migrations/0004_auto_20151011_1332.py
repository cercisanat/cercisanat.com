# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_issue', '0003_auto_20151003_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='cover_video',
            field=models.FileField(upload_to=b'videos/issue/', null=True, verbose_name='Cover Video', blank=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 10, 32, 37, 292927, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
    ]
