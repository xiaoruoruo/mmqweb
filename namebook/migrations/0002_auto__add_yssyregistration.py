# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'YssyRegistration'
        db.create_table('namebook_yssyregistration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('yssyid', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('namebook', ['YssyRegistration'])


    def backwards(self, orm):
        # Deleting model 'YssyRegistration'
        db.delete_table('namebook_yssyregistration')


    models = {
        'namebook.entity': {
            'Meta': {'object_name': 'Entity'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories_rel_+'", 'blank': 'True', 'to': "orm['namebook.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'redirect': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['namebook.Entity']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'namebook.yssyregistration': {
            'Meta': {'object_name': 'YssyRegistration'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'yssyid': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['namebook']