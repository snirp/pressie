# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complex',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('naam', models.CharField(max_length=60)),
                ('code', models.CharField(max_length=20)),
                ('foto', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ['code'],
                'verbose_name_plural': 'Complexen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complexdeel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('meeteenheid', models.IntegerField(choices=[(1, '%'), (2, 'm'), (3, 'm2'), (5, 'st')])),
                ('onderhoudsjaar', models.IntegerField()),
            ],
            options={
                'ordering': ['complexgroep', 'element'],
                'verbose_name_plural': 'Complexdelen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complexgroep',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('beschrijving', models.TextField(null=True, blank=True)),
                ('complex', models.ForeignKey(to='gebouw.Complex')),
                ('hoofdgroep', models.ForeignKey(to='stam.Hoofdgroep')),
            ],
            options={
                'ordering': ['hoofdgroep'],
                'verbose_name_plural': 'Complexgroepen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditiedeel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('conditiescore', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
            ],
            options={
                'ordering': ['deel'],
                'verbose_name_plural': 'Conditiedelen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditiefoto',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('foto_link', models.URLField()),
                ('conditiedeel', models.ForeignKey(to='gebouw.Conditiedeel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditiegroep',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('bevinding', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['scenariogroep'],
                'verbose_name_plural': 'Conditiegroepen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditiemeting',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('datum', models.DateField()),
                ('uitvoerder', models.CharField(max_length=80, null=True, blank=True)),
            ],
            options={
                'ordering': ['-datum'],
                'verbose_name_plural': 'Conditiemetingen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('naam', models.CharField(max_length=80)),
                ('hvh', models.FloatField()),
                ('stravis_scdeel', models.IntegerField(null=True, blank=True)),
                ('complexdeel', models.ForeignKey(to='gebouw.Complexdeel')),
            ],
            options={
                'ordering': ['naam'],
                'verbose_name_plural': 'Delen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gebrek',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('naam', models.CharField(max_length=80)),
                ('ernst', models.IntegerField(null=True, blank=True, choices=[(1, 'Gering'), (2, 'Serieus'), (3, 'Ernstig')])),
                ('omvang', models.IntegerField(choices=[(0, '< 2%'), (1, '2% tot 10%'), (2, '10% tot 30%'), (3, '30% tot 70%'), (4, '> 70%')])),
                ('intensiteit', models.IntegerField(choices=[(1, 'Laag'), (2, 'Midden'), (3, 'Hoog')])),
                ('conditiedeel', models.ForeignKey(to='gebouw.Conditiedeel')),
                ('nengebrek', models.ForeignKey(null=True, blank=True, to='stam.Nengebrek')),
            ],
            options={
                'verbose_name_plural': 'Gebreken',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Maatregel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('naam', models.CharField(max_length=80)),
                ('ehprijs', models.DecimalField(decimal_places=2, max_digits=8)),
                ('uitvoer_percentage', models.IntegerField(default=100)),
                ('start', models.IntegerField()),
                ('cyclus', models.IntegerField()),
                ('eind', models.IntegerField()),
                ('opmerking', models.CharField(max_length=200, null=True, blank=True)),
                ('stravis_scnmr', models.IntegerField(null=True, blank=True)),
                ('activiteit', models.ForeignKey(to='stam.Activiteit')),
            ],
            options={
                'ordering': ['naam'],
                'verbose_name_plural': 'Maatregelen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('naam', models.CharField(max_length=80)),
                ('start', models.IntegerField()),
                ('eind', models.IntegerField()),
                ('complex', models.ForeignKey(to='gebouw.Complex')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scenariogroep',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('complexgroep', models.ForeignKey(to='gebouw.Complexgroep')),
                ('scenario', models.ForeignKey(to='gebouw.Scenario')),
            ],
            options={
                'ordering': ['complexgroep'],
                'verbose_name_plural': 'Scenariogroepen',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deel',
            name='scenariogroep',
            field=models.ForeignKey(to='gebouw.Scenariogroep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiemeting',
            name='scenario',
            field=models.OneToOneField(null=True, blank=True, to='gebouw.Scenario'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiegroep',
            name='conditiemeting',
            field=models.ForeignKey(to='gebouw.Conditiemeting'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiegroep',
            name='scenariogroep',
            field=models.OneToOneField(null=True, blank=True, to='gebouw.Scenariogroep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiedeel',
            name='conditiegroep',
            field=models.ForeignKey(to='gebouw.Conditiegroep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiedeel',
            name='deel',
            field=models.OneToOneField(null=True, blank=True, to='gebouw.Deel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complexdeel',
            name='complexgroep',
            field=models.ForeignKey(to='gebouw.Complexgroep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complexdeel',
            name='element',
            field=models.ForeignKey(null=True, blank=True, to='stam.Element'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complex',
            name='actueel_scenario',
            field=models.OneToOneField(related_name='actueel', to='gebouw.Scenario'),
            preserve_default=True,
        ),
    ]
