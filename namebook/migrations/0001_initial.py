# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Entity'
        db.create_table('namebook_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('redirect', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['namebook.Entity'], null=True, blank=True)),
        ))
        db.send_create_signal('namebook', ['Entity'])

        # Adding M2M table for field categories on 'Entity'
        db.create_table('namebook_entity_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_entity', models.ForeignKey(orm['namebook.entity'], null=False)),
            ('to_entity', models.ForeignKey(orm['namebook.entity'], null=False))
        ))
        db.create_unique('namebook_entity_categories', ['from_entity_id', 'to_entity_id'])


    def backwards(self, orm):
        # Deleting model 'Entity'
        db.delete_table('namebook_entity')

        # Removing M2M table for field categories on 'Entity'
        db.delete_table('namebook_entity_categories')


    models = {
        'namebook.entity': {
            'Meta': {'object_name': 'Entity'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories_rel_+'", 'blank': 'True', 'to': "orm['namebook.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'redirect': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['namebook.Entity']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['namebook']