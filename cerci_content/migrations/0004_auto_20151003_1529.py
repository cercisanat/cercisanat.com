# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_content', '0003_auto_20150406_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 3, 12, 29, 49, 976266, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='author',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField(b'image', '360x360', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping'),
        ),
        migrations.AlterField(
            model_name='issuecontent',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 3, 12, 29, 49, 978041, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi'),
        ),
    ]
