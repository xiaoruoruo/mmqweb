# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Member.balance'
        db.add_column('club_member', 'balance',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'Activity.cost'
        db.add_column('club_activity', 'cost',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'Activity.deposit'
        db.add_column('club_activity', 'deposit',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Member.balance'
        db.delete_column('club_member', 'balance')

        # Deleting field 'Activity.cost'
        db.delete_column('club_activity', 'cost')

        # Deleting field 'Activity.deposit'
        db.delete_column('club_activity', 'deposit')


    models = {
        'club.activity': {
            'Meta': {'object_name': 'Activity'},
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 10, 24, 0, 0)'}),
            'deposit': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['club.Member']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.0'})
        },
        'club.member': {
            'Meta': {'object_name': 'Member'},
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        }
    }

    complete_apps = ['club']