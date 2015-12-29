# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.FloatField(default=1.0)),
                ('date', models.DateField(default=datetime.date(2015, 12, 26))),
                ('cost', models.FloatField(blank=True)),
                ('deposit', models.FloatField(null=True, blank=True)),
                ('comment', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('male', models.BooleanField()),
                ('affiliation', models.CharField(max_length=20, null=True, blank=True)),
                ('weight', models.FloatField(default=0.0)),
                ('balance', models.FloatField(default=0.0)),
                ('hidden', models.BooleanField(default=False)),
                ('hidden_date', models.DateField(null=True)),
                ('cost_override', models.FloatField(null=True, blank=True)),
                ('extra', models.TextField(default=b'{}')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='member',
            field=models.ForeignKey(to='club.Member'),
            preserve_default=True,
        ),
    ]
