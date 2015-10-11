# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_newsletters', '0003_auto_20151003_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 10, 32, 37, 305036, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 10, 32, 37, 302459, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False),
        ),
        migrations.AlterField(
            model_name='unsubscribetoken',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 10, 32, 37, 303934, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False),
        ),
    ]
