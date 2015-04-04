# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 7, 38, 32, 280787, tzinfo=utc), verbose_name='Created At', editable=False)),
                ('updated_at', models.DateTimeField(verbose_name='Updated At', editable=False)),
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
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 7, 38, 32, 278617, tzinfo=utc), verbose_name='Created At', editable=False)),
                ('updated_at', models.DateTimeField(verbose_name='Updated At', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='UnsubscribeToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=16, verbose_name='Token')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 4, 4, 7, 38, 32, 279855, tzinfo=utc), verbose_name='Created At', editable=False)),
                ('updated_at', models.DateTimeField(verbose_name='Updated At', editable=False)),
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
