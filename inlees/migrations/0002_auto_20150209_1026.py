# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onderhoud', '0003_auto_20150209_1026'),
        ('inlees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConditiemetingLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('conditiemeting_stravis', models.PositiveIntegerField()),
                ('conditiemeting', models.OneToOneField(to='onderhoud.Conditiemeting')),
                ('database', models.ForeignKey(to='inlees.StravisDatabase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeelcomplexLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('deelcomplex_stravis', models.PositiveIntegerField()),
                ('complex', models.OneToOneField(to='onderhoud.Complex')),
                ('database', models.ForeignKey(to='inlees.StravisDatabase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImportScenario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('sc_stravis', models.PositiveIntegerField()),
                ('sc_start', models.PositiveIntegerField()),
                ('sc_naam', models.CharField(max_length=80)),
                ('dc_stravis', models.PositiveIntegerField()),
                ('dc_code', models.CharField(max_length=20)),
                ('dc_naam', models.CharField(max_length=60)),
                ('dc_functie', models.CharField(max_length=40, blank=True, null=True)),
                ('dc_aantal_eh', models.PositiveIntegerField(null=True, blank=True)),
                ('dc_bouwjaar', models.PositiveIntegerField(null=True, blank=True)),
                ('dc_straat', models.CharField(max_length=80, blank=True, null=True)),
                ('dc_huisnummer', models.CharField(max_length=20, blank=True, null=True)),
                ('dc_plaats', models.CharField(max_length=60, blank=True, null=True)),
                ('cm_stravis', models.PositiveIntegerField(null=True, blank=True)),
                ('cm_datum', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScenarioLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('scenario_stravis', models.PositiveIntegerField()),
                ('database', models.ForeignKey(to='inlees.StravisDatabase')),
                ('scenario', models.OneToOneField(to='onderhoud.Scenario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='conditiedeellink',
            name='database',
            field=models.ForeignKey(default=1, to='inlees.StravisDatabase'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deellink',
            name='database',
            field=models.ForeignKey(default=1, to='inlees.StravisDatabase'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='importdeel',
            name='sc_stravis',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
