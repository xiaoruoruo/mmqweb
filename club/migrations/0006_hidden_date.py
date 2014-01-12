# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

import reversion
LATEST = 0

class Migration(DataMigration):

    def forwards(self, orm):
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        # Gets the hidden date from reversion data
        for hiddenMember in orm.Member.objects.filter(hidden=True):
            hiddenMember.hidden_date = reversion.get_for_object(hiddenMember)[LATEST].revision.date_created
            hiddenMember.save()


    def backwards(self, orm):
        pass

    models = {
        u'club.activity': {
            'Meta': {'object_name': 'Activity'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 1, 13, 0, 0)'}),
            'deposit': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['club.Member']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.0'})
        },
        u'club.member': {
            'Meta': {'object_name': 'Member'},
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        }
    }

    complete_apps = ['club']
    symmetrical = True
