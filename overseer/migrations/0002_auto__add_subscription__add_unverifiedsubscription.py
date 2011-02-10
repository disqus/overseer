# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Subscription'
        db.create_table('overseer_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal('overseer', ['Subscription'])

        # Adding M2M table for field services on 'Subscription'
        db.create_table('overseer_subscription_services', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscription', models.ForeignKey(orm['overseer.subscription'], null=False)),
            ('service', models.ForeignKey(orm['overseer.service'], null=False))
        ))
        db.create_unique('overseer_subscription_services', ['subscription_id', 'service_id'])

        # Adding model 'UnverifiedSubscription'
        db.create_table('overseer_unverifiedsubscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('overseer', ['UnverifiedSubscription'])

        # Adding M2M table for field services on 'UnverifiedSubscription'
        db.create_table('overseer_unverifiedsubscription_services', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('unverifiedsubscription', models.ForeignKey(orm['overseer.unverifiedsubscription'], null=False)),
            ('service', models.ForeignKey(orm['overseer.service'], null=False))
        ))
        db.create_unique('overseer_unverifiedsubscription_services', ['unverifiedsubscription_id', 'service_id'])


    def backwards(self, orm):
        
        # Deleting model 'Subscription'
        db.delete_table('overseer_subscription')

        # Removing M2M table for field services on 'Subscription'
        db.delete_table('overseer_subscription_services')

        # Deleting model 'UnverifiedSubscription'
        db.delete_table('overseer_unverifiedsubscription')

        # Removing M2M table for field services on 'UnverifiedSubscription'
        db.delete_table('overseer_unverifiedsubscription_services')


    models = {
        'overseer.event': {
            'Meta': {'object_name': 'Event'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'peak_status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['overseer.Service']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'overseer.eventupdate': {
            'Meta': {'object_name': 'EventUpdate'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['overseer.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'overseer.service': {
            'Meta': {'ordering': "('order', 'name')", 'object_name': 'Service'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'overseer.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['overseer.Service']", 'symmetrical': 'False'})
        },
        'overseer.unverifiedsubscription': {
            'Meta': {'object_name': 'UnverifiedSubscription'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['overseer.Service']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['overseer']
