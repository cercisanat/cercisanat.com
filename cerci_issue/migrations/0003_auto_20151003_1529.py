# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_issue', '0002_auto_20150404_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='cover_video',
            field=models.FileField(upload_to=b'videos/issue/', null=True, verbose_name='Cover Video'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 3, 12, 29, 49, 988013, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
    ]
