# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_issue', '0003_auto_20150404_1737'),
        ('cerci_newsletters', '0002_auto_20150404_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='body',
        ),
        migrations.AddField(
            model_name='newsletter',
            name='issue',
            field=models.ForeignKey(default=1, to='cerci_issue.Issue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsletter',
            name='template',
            field=models.CharField(default='email/newsletters.html', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 14, 36, 40, 992626, tzinfo=utc), verbose_name='Created At', editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 14, 36, 40, 989850, tzinfo=utc), verbose_name='Created At', editable=False),
        ),
        migrations.AlterField(
            model_name='unsubscribetoken',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 4, 14, 36, 40, 991189, tzinfo=utc), verbose_name='Created At', editable=False),
        ),
    ]
