# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activiteit',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('naam', models.CharField(max_length=80)),
                ('normprijs', models.DecimalField(max_digits=8, decimal_places=2)),
                ('btw', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
            options={
                'ordering': ['naam'],
                'verbose_name_plural': 'Activiteiten',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Codering',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=4)),
                ('naam', models.CharField(max_length=60)),
            ],
            options={
                'ordering': ['code'],
                'verbose_name_plural': 'Coderingen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('naam', models.CharField(max_length=60)),
                ('codering', models.ForeignKey(to='stam.Codering')),
            ],
            options={
                'ordering': ['codering', 'naam'],
                'verbose_name_plural': 'Elementen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gebrektype',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('naam', models.CharField(max_length=50)),
                ('ernst', models.IntegerField(choices=[(1, 'Gering'), (2, 'Serieus'), (3, 'Ernstig')])),
            ],
            options={
                'ordering': ['ernst', 'naam'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hoofdgroep',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('naam', models.CharField(max_length=50)),
                ('order', models.IntegerField()),
                ('stravis_hoofdgroep', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'Hoofdgroepen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nengebrek',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('naam', models.CharField(max_length=60)),
                ('gebrektype', models.ForeignKey(to='stam.Gebrektype')),
            ],
            options={
                'ordering': ['naam'],
                'verbose_name_plural': 'Nengebreken',
            },
            bases=(models.Model,),
        ),
    ]
