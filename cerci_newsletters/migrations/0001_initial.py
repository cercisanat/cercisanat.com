# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subscriber'
        db.create_table(u'cerci_newsletters_subscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 19, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'cerci_newsletters', ['Subscriber'])

        # Adding model 'Newsletter'
        db.create_table(u'cerci_newsletters_newsletter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 19, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'cerci_newsletters', ['Newsletter'])

        # Adding model 'SentItem'
        db.create_table(u'cerci_newsletters_sentitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('newsletter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cerci_newsletters.Newsletter'])),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_to', to=orm['cerci_newsletters.Subscriber'])),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'cerci_newsletters', ['SentItem'])

        # Adding unique constraint on 'SentItem', fields ['newsletter', 'subscriber']
        db.create_unique(u'cerci_newsletters_sentitem', ['newsletter_id', 'subscriber_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'SentItem', fields ['newsletter', 'subscriber']
        db.delete_unique(u'cerci_newsletters_sentitem', ['newsletter_id', 'subscriber_id'])

        # Deleting model 'Subscriber'
        db.delete_table(u'cerci_newsletters_subscriber')

        # Deleting model 'Newsletter'
        db.delete_table(u'cerci_newsletters_newsletter')

        # Deleting model 'SentItem'
        db.delete_table(u'cerci_newsletters_sentitem')


    models = {
        u'cerci_newsletters.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 19, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'cerci_newsletters.sentitem': {
            'Meta': {'unique_together': "(('newsletter', 'subscriber'),)", 'object_name': 'SentItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsletter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cerci_newsletters.Newsletter']"}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_to'", 'to': u"orm['cerci_newsletters.Subscriber']"})
        },
        u'cerci_newsletters.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 19, 0, 0)'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['cerci_newsletters']