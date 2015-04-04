# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_newsletters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 7, 58, 27, 980840, tzinfo=utc), verbose_name='Created At', editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 7, 58, 27, 979368, tzinfo=utc), verbose_name='Created At', editable=False),
        ),
        migrations.AlterField(
            model_name='unsubscribetoken',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 7, 58, 27, 980111, tzinfo=utc), verbose_name='Created At', editable=False),
        ),
    ]
