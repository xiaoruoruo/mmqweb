# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tournament'
        db.create_table('game_tournament', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('extra', self.gf('django.db.models.fields.TextField')(default='{}')),
        ))
        db.send_create_signal('game', ['Tournament'])

        # Adding M2M table for field participants on 'Tournament'
        db.create_table('game_tournament_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tournament', models.ForeignKey(orm['game.tournament'], null=False)),
            ('participation', models.ForeignKey(orm['game.participation'], null=False))
        ))
        db.create_unique('game_tournament_participants', ['tournament_id', 'participation_id'])

        # Adding model 'Participation'
        db.create_table('game_participation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('displayname', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player', to=orm['namebook.Entity'])),
            ('represent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='represent', null=True, to=orm['namebook.Entity'])),
        ))
        db.send_create_signal('game', ['Participation'])

        # Adding model 'Ranking'
        db.create_table('game_ranking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('game', ['Ranking'])

        # Adding M2M table for field matches on 'Ranking'
        db.create_table('game_ranking_matches', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ranking', models.ForeignKey(orm['game.ranking'], null=False)),
            ('match', models.ForeignKey(orm['game.match'], null=False))
        ))
        db.create_unique('game_ranking_matches', ['ranking_id', 'match_id'])

        # Adding model 'MatchGroup'
        db.create_table('game_matchgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Tournament'])),
            ('ranking', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Ranking'], null=True, blank=True)),
            ('view_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('game', ['MatchGroup'])

        # Adding model 'Match'
        db.create_table('game_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.MatchGroup'], null=True, blank=True)),
            ('result', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('player11', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player11', to=orm['namebook.Entity'])),
            ('player12', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='player12', null=True, to=orm['namebook.Entity'])),
            ('player21', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player21', to=orm['namebook.Entity'])),
            ('player22', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='player22', null=True, to=orm['namebook.Entity'])),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('extra', self.gf('django.db.models.fields.TextField')(default='{}')),
        ))
        db.send_create_signal('game', ['Match'])

        # Adding model 'Game'
        db.create_table('game_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Match'])),
            ('score1', self.gf('django.db.models.fields.IntegerField')()),
            ('score2', self.gf('django.db.models.fields.IntegerField')()),
            ('extra', self.gf('django.db.models.fields.TextField')(default='{}')),
        ))
        db.send_create_signal('game', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Tournament'
        db.delete_table('game_tournament')

        # Removing M2M table for field participants on 'Tournament'
        db.delete_table('game_tournament_participants')

        # Deleting model 'Participation'
        db.delete_table('game_participation')

        # Deleting model 'Ranking'
        db.delete_table('game_ranking')

        # Removing M2M table for field matches on 'Ranking'
        db.delete_table('game_ranking_matches')

        # Deleting model 'MatchGroup'
        db.delete_table('game_matchgroup')

        # Deleting model 'Match'
        db.delete_table('game_match')

        # Deleting model 'Game'
        db.delete_table('game_game')


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
            'ranking': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['game.Ranking']", 'null': 'True', 'blank': 'True'}),
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
        'game.ranking': {
            'Meta': {'object_name': 'Ranking'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matches': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['game.Match']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'game.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'extra': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tournaments'", 'symmetrical': 'False', 'to': "orm['game.Participation']"}),
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