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
        migrations.AddField(
            model_name='subscriber',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 15, 18, 13, 14, 187958, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 15, 18, 13, 14, 184147, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False),
        ),
        migrations.AlterField(
            model_name='unsubscribetoken',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 15, 18, 13, 14, 185760, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False),
        ),
    ]
