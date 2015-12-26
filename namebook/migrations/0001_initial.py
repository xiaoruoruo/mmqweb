# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.IntegerField(null=True, choices=[(1, '\u7537\u751f'), (2, '\u5973\u751f'), (3, '\u56e2\u4f53')])),
                ('text', models.TextField(blank=True)),
                ('categories', models.ManyToManyField(related_name='categories_rel_+', to='namebook.Entity', blank=True)),
                ('redirect', models.ForeignKey(blank=True, to='namebook.Entity', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YssyRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yssyid', models.CharField(max_length=12)),
                ('date', models.DateField()),
                ('code', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
