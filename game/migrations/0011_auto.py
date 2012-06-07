# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field admins on 'Tournament'
        db.create_table('game_tournament_admins', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tournament', models.ForeignKey(orm['game.tournament'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('game_tournament_admins', ['tournament_id', 'user_id'])


    def backwards(self, orm):
        # Removing M2M table for field admins on 'Tournament'
        db.delete_table('game_tournament_admins')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'game.game': {
            'Meta': {'object_name': 'Game'},
            'extra': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.Match']"}),
            'score1': ('django.db.models.fields.IntegerField', [], {}),
            'score2': ('django.db.models.fields.IntegerField', [], {})
        },
        'game.match': {
            'Meta': {'object_name': 'Match'},
            'extra': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.MatchGroup']", 'null': 'True', 'blank': 'True'}),
            'player11': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player11'", 'to': "orm['namebook.Entity']"}),
            'player12': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'player12'", 'null': 'True', 'to': "orm['namebook.Entity']"}),
            'player21': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player21'", 'to': "orm['namebook.Entity']"}),
            'player22': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'player22'", 'null': 'True', 'to': "orm['namebook.Entity']"}),
            'result': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'game.matchgroup': {
            'Meta': {'object_name': 'MatchGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.Tournament']"}),
            'view_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'game.participation': {
            'Meta': {'object_name': 'Participation'},
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player'", 'to': "orm['namebook.Entity']"}),
            'represent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'represent'", 'null': 'True', 'to': "orm['namebook.Entity']"})
        },
        'game.personalrating': {
            'Meta': {'object_name': 'PersonalRating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.Match']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['namebook.Entity']"}),
            'ranking': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.Ranking']"}),
            'rating_doubles': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rating_singles': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'game.ranking': {
            'Meta': {'object_name': 'Ranking'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mg': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.MatchGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'game.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'extra': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tournaments'", 'blank': 'True', 'to': "orm['game.Participation']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
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

    complete_apps = ['game']