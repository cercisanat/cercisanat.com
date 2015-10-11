# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_content', '0004_auto_20151003_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 10, 32, 37, 280324, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='issuecontent',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 10, 32, 37, 283056, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
    ]
