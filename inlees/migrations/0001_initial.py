# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onderhoud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConditiedeelLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('deel_stravis', models.PositiveIntegerField()),
                ('conditiedeel', models.OneToOneField(to='onderhoud.Conditiedeel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeelLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('scenariodeel_stravis', models.PositiveIntegerField()),
                ('deel', models.OneToOneField(to='onderhoud.Deel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImportDeel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('deel_stravis', models.PositiveIntegerField(blank=True, null=True)),
                ('scenariodeel_stravis', models.PositiveIntegerField()),
                ('hoofdgroep_stravis', models.PositiveIntegerField()),
                ('naam', models.CharField(max_length=80)),
                ('schilderjaar', models.PositiveIntegerField(blank=True, null=True)),
                ('vervangjaar', models.PositiveIntegerField(blank=True, null=True)),
                ('hvh_sw', models.FloatField(blank=True, null=True)),
                ('hvh_ogr', models.FloatField(blank=True, null=True)),
                ('element_stravis', models.PositiveIntegerField()),
                ('eh_sw', models.PositiveIntegerField(blank=True, null=True)),
                ('eh_ogr', models.PositiveIntegerField()),
                ('conditie_sw', models.PositiveIntegerField(blank=True, null=True)),
                ('conditie_ogr', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Import delen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImportGebrek',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('gemeten_stravis', models.PositiveIntegerField()),
                ('deel_stravis', models.PositiveIntegerField()),
                ('gebrek_stravis', models.PositiveIntegerField()),
                ('gebrektype', models.PositiveIntegerField()),
                ('naam', models.CharField(max_length=80)),
                ('omvang', models.PositiveIntegerField()),
                ('intensiteit', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name_plural': 'Import gebreken',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImportMaatregel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('scenariomaatregel_stravis', models.PositiveIntegerField()),
                ('scenariodeel_stravis', models.PositiveIntegerField()),
                ('activiteit_stravis', models.PositiveIntegerField()),
                ('eenheid', models.PositiveIntegerField()),
                ('naam', models.CharField(max_length=80)),
                ('eh_prijs_excl', models.DecimalField(max_digits=8, decimal_places=2)),
                ('eh_prijs_incl', models.DecimalField(max_digits=8, decimal_places=2)),
                ('relatief', models.BooleanField(default=True)),
                ('hvh_uitvoer', models.FloatField()),
                ('start', models.PositiveIntegerField()),
                ('cyclus', models.PositiveIntegerField()),
                ('eind', models.PositiveIntegerField()),
                ('opmerking', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Import maatregelen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StravisDatabase',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('naam', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VertaalActiviteit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('activiteit_stravis', models.PositiveIntegerField()),
                ('activiteit', models.ForeignKey(to='onderhoud.Activiteit')),
                ('database', models.ForeignKey(to='inlees.StravisDatabase')),
            ],
            options={
                'verbose_name_plural': 'Vertaal activiteiten',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VertaalElement',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('element_stravis', models.PositiveIntegerField()),
                ('omrekenfactor', models.FloatField(default=1.0)),
                ('database', models.ForeignKey(to='inlees.StravisDatabase')),
                ('element', models.ForeignKey(to='onderhoud.Element')),
            ],
            options={
                'verbose_name_plural': 'Vertaal Elementen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VertaalGebrek',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('gebrek_stravis', models.PositiveIntegerField()),
                ('database', models.ForeignKey(to='inlees.StravisDatabase')),
                ('nengebrek', models.ForeignKey(to='onderhoud.Nengebrek')),
            ],
            options={
                'verbose_name_plural': 'Vertaal gebreken',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VertaalGebrektype',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('gebrektype_stravis', models.PositiveIntegerField()),
                ('database', models.ForeignKey(to='inlees.StravisDatabase')),
                ('gebrektype', models.OneToOneField(to='onderhoud.Gebrektype')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VertaalHoofdgroep',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('hoofdgroep_stravis', models.PositiveIntegerField()),
                ('naam_stravis', models.CharField(blank=True, max_length=80, null=True)),
                ('database', models.ForeignKey(to='inlees.StravisDatabase')),
                ('hoofdgroep', models.ForeignKey(to='onderhoud.Hoofdgroep')),
            ],
            options={
                'ordering': ['hoofdgroep_stravis'],
            },
            bases=(models.Model,),
        ),
    ]
