# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_content', '0002_auto_20150404_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 6, 19, 54, 10, 510859, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='issuecontent',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 6, 19, 54, 10, 513105, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='issuecontent',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Yay\u0131nda m\u0131'),
        ),
    ]
