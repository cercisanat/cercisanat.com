# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_newsletters', '0002_auto_20150415_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 3, 12, 29, 49, 999278, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 3, 12, 29, 49, 996849, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False),
        ),
        migrations.AlterField(
            model_name='unsubscribetoken',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 3, 12, 29, 49, 998042, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False),
        ),
    ]
