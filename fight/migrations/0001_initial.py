# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameRecord'
        db.create_table('fight_gamerecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('json', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('fight', ['GameRecord'])


    def backwards(self, orm):
        # Deleting model 'GameRecord'
        db.delete_table('fight_gamerecord')


    models = {
        'fight.gamerecord': {
            'Meta': {'object_name': 'GameRecord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'json': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['fight']