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
        migrations.AlterField(
            model_name='author',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 20, 4, 8, 591211, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='issuecontent',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 20, 4, 8, 593082, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
    ]
