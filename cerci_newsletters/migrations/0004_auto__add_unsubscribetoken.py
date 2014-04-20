# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UnsubscribeToken'
        db.create_table(u'cerci_newsletters_unsubscribetoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cerci_newsletters.Subscriber'])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('is_used', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 20, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'cerci_newsletters', ['UnsubscribeToken'])


    def backwards(self, orm):
        # Deleting model 'UnsubscribeToken'
        db.delete_table(u'cerci_newsletters_unsubscribetoken')


    models = {
        u'cerci_newsletters.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 20, 0, 0)'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 20, 0, 0)'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'cerci_newsletters.unsubscribetoken': {
            'Meta': {'object_name': 'UnsubscribeToken'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cerci_newsletters.Subscriber']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['cerci_newsletters']