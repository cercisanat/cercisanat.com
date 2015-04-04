# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cerci_issue', '0002_auto_20150404_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Ba\u015fl\u0131k')),
                ('template', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 20, 4, 17, 869363, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False)),
                ('updated_at', models.DateTimeField(verbose_name='G\xfcncelleme Tarihi', editable=False)),
                ('issue', models.ForeignKey(to='cerci_issue.Issue')),
            ],
        ),
        migrations.CreateModel(
            name='SentItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent_at', models.DateTimeField(verbose_name='Sent At')),
                ('newsletter', models.ForeignKey(verbose_name='Newsletter', to='cerci_newsletters.Newsletter')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='\u0130sim', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 20, 4, 17, 867363, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False)),
                ('updated_at', models.DateTimeField(verbose_name='G\xfcncelleme Tarihi', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='UnsubscribeToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=16, verbose_name='Token')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 20, 4, 17, 868127, tzinfo=utc), verbose_name='Olu\u015fturulma Tarihi', editable=False)),
                ('updated_at', models.DateTimeField(verbose_name='G\xfcncelleme Tarihi', editable=False)),
                ('subscriber', models.ForeignKey(verbose_name='Subscriber', to='cerci_newsletters.Subscriber', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='sentitem',
            name='subscriber',
            field=models.ForeignKey(related_name='sent_to', verbose_name='Subscriber', to='cerci_newsletters.Subscriber'),
        ),
        migrations.AlterUniqueTogether(
            name='sentitem',
            unique_together=set([('newsletter', 'subscriber')]),
        ),
    ]
