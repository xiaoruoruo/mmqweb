# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Rating'
        db.delete_table('game_rating')

        # Adding model 'PersonalRating'
        db.create_table('game_personalrating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['namebook.Entity'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Match'])),
            ('rating_singles', self.gf('django.db.models.fields.FloatField')()),
            ('rating_doubles', self.gf('django.db.models.fields.FloatField')()),
            ('rating_mixed', self.gf('django.db.models.fields.FloatField')()),
            ('mg', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.MatchGroup'])),
        ))
        db.send_create_signal('game', ['PersonalRating'])


    def backwards(self, orm):
        # Adding model 'Rating'
        db.create_table('game_rating', (
            ('rating', self.gf('django.db.models.fields.FloatField')()),
            ('player1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player1', to=orm['namebook.Entity'])),
            ('player2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player2', null=True, to=orm['namebook.Entity'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Match'])),
        ))
        db.send_create_signal('game', ['Rating'])

        # Deleting model 'PersonalRating'
        db.delete_table('game_personalrating')


    models = {
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
            'mg': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.MatchGroup']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['namebook.Entity']"}),
            'rating_doubles': ('django.db.models.fields.FloatField', [], {}),
            'rating_mixed': ('django.db.models.fields.FloatField', [], {}),
            'rating_singles': ('django.db.models.fields.FloatField', [], {})
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