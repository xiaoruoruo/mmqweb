# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('namebook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score1', models.IntegerField()),
                ('score2', models.IntegerField()),
                ('extra', models.TextField(default=b'{}')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.IntegerField(null=True, blank=True)),
                ('type', models.IntegerField(choices=[(1, b'Team'), (2, b'\xe5\x8d\x95\xe6\x89\x93'), (3, b'\xe5\x8f\x8c\xe6\x89\x93'), (4, b'\xe4\xb8\x80\xe6\x89\x93\xe4\xba\x8c')])),
                ('text', models.TextField(blank=True)),
                ('extra', models.TextField(default=b'{}')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('view_name', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('displayname', models.CharField(max_length=50, blank=True)),
                ('player', models.ForeignKey(related_name='player', to='namebook.Entity')),
                ('represent', models.ForeignKey(related_name='represent', blank=True, to='namebook.Entity', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonalRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating_singles', models.FloatField(null=True)),
                ('rating_doubles', models.FloatField(null=True)),
                ('match', models.ForeignKey(to='game.Match')),
                ('player', models.ForeignKey(to='namebook.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(choices=[(1, b'\xe5\x8d\x95\xe6\xb7\x98\xe6\xb1\xb0'), (2, b'\xe5\x8d\x95\xe5\xbe\xaa\xe7\x8e\xaf'), (3, b'2n-1\xe5\xb1\x80n\xe8\x83\x9c'), (4, b'\xe4\xb8\xaa\xe4\xba\xba\xe6\x8e\x92\xe5\x90\x8d(fish)'), (5, b'\xe4\xb8\xaa\xe4\xba\xba\xe6\x8e\x92\xe5\x90\x8d(elo)')])),
                ('name', models.CharField(max_length=50, blank=True)),
                ('mg', models.ForeignKey(to='game.MatchGroup')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('text', models.TextField(blank=True)),
                ('extra', models.TextField(default=b'{}')),
                ('admins', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
                ('participants', models.ManyToManyField(related_name='tournaments', to='game.Participation', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='personalrating',
            name='ranking',
            field=models.ForeignKey(to='game.Ranking'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='matchgroup',
            name='tournament',
            field=models.ForeignKey(to='game.Tournament'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='match_group',
            field=models.ForeignKey(blank=True, to='game.MatchGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='player11',
            field=models.ForeignKey(related_name='player11', to='namebook.Entity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='player12',
            field=models.ForeignKey(related_name='player12', blank=True, to='namebook.Entity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='player21',
            field=models.ForeignKey(related_name='player21', to='namebook.Entity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='player22',
            field=models.ForeignKey(related_name='player22', blank=True, to='namebook.Entity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='match',
            field=models.ForeignKey(to='game.Match'),
            preserve_default=True,
        ),
    ]
