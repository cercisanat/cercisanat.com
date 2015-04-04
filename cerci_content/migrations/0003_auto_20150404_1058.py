# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_content', '0002_auto_20150404_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 7, 58, 27, 961444, tzinfo=utc), verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='issuecontent',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 7, 58, 27, 963681, tzinfo=utc), verbose_name='Created At'),
        ),
    ]
