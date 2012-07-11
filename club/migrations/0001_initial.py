# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table('club_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('male', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('affiliation', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('club', ['Member'])

        # Adding model 'Activity'
        db.create_table('club_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['club.Member'])),
            ('weight', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('club', ['Activity'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table('club_member')

        # Deleting model 'Activity'
        db.delete_table('club_activity')


    models = {
        'club.activity': {
            'Meta': {'object_name': 'Activity'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['club.Member']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.0'})
        },
        'club.member': {
            'Meta': {'object_name': 'Member'},
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['club']