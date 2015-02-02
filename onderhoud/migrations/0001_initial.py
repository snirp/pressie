# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activiteit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=80)),
                ('eenheid', models.IntegerField(choices=[(1, '%'), (2, 'm'), (3, 'm2'), (5, 'st'), (6, 'won'), (7, 'verd'), (8, 'zijde'), (9, 'post')])),
                ('generiek', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Activiteiten',
                'ordering': ['naam'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActiviteitOnderbouwing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('hoeveelheid', models.FloatField(default=1.0)),
                ('activiteit', models.ForeignKey(to='onderhoud.Activiteit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Btw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=20)),
                ('percentage', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Codering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('code', models.CharField(max_length=4)),
                ('naam', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Coderingen',
                'ordering': ['code'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=60)),
                ('code', models.CharField(max_length=20)),
                ('foto', models.ImageField(upload_to='complex', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Complexen',
                'ordering': ['code'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complexdeel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('onderhoudsjaar', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Complexdelen',
                'ordering': ['complexgroep', 'element'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complexgroep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('beschrijving', models.TextField(blank=True, null=True)),
                ('naam', models.TextField(max_length=80)),
                ('complex', models.ForeignKey(to='onderhoud.Complex')),
            ],
            options={
                'verbose_name_plural': 'Complexgroepen',
                'ordering': ['complex', 'hoofdgroep'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditiedeel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('conditiescore', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])),
            ],
            options={
                'verbose_name_plural': 'Conditiedelen',
                'ordering': ['deel'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditiefoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('foto', models.ImageField(upload_to='images')),
                ('conditiedeel', models.ForeignKey(to='onderhoud.Conditiedeel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditiegroep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('bevinding', models.TextField(blank=True, null=True)),
                ('conditie', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], default=1)),
            ],
            options={
                'verbose_name_plural': 'Conditiegroepen',
                'ordering': ['scenariogroep'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditiemeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('datum', models.DateField()),
                ('uitvoerder', models.CharField(blank=True, null=True, max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Conditiemetingen',
                'ordering': ['-datum'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=80)),
                ('hvh', models.FloatField()),
                ('start', models.PositiveIntegerField(blank=True, null=True)),
                ('eind', models.PositiveIntegerField(blank=True, null=True)),
                ('complexdeel', models.ForeignKey(to='onderhoud.Complexdeel')),
            ],
            options={
                'verbose_name_plural': 'Delen',
                'ordering': ['scenariogroep', 'naam'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deelactiviteit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=80)),
                ('beschrijving', models.TextField(blank=True, null=True)),
                ('eh_prijs', models.DecimalField(max_digits=8, decimal_places=2)),
                ('eenheid', models.IntegerField(choices=[(1, '%'), (2, 'm'), (3, 'm2'), (5, 'st'), (6, 'won'), (7, 'verd'), (8, 'zijde'), (9, 'post')])),
                ('btw', models.ForeignKey(to='onderhoud.Btw')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=60)),
                ('eenheid', models.IntegerField(choices=[(1, '%'), (2, 'm'), (3, 'm2'), (5, 'st'), (6, 'won'), (7, 'verd'), (8, 'zijde'), (9, 'post')])),
                ('vervangwaarde', models.PositiveIntegerField(default=1)),
                ('steekwoorden', models.CharField(blank=True, null=True, max_length=100)),
                ('omschrijving', models.TextField(blank=True, null=True)),
                ('generiek', models.BooleanField(default=False)),
                ('codering', models.ForeignKey(to='onderhoud.Codering')),
                ('standaard_activiteiten', models.ManyToManyField(blank=True, to='onderhoud.Activiteit', null=True)),
            ],
            options={
                'verbose_name_plural': 'Elementen',
                'ordering': ['codering', 'naam'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gebrek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=80)),
                ('omvang', models.IntegerField(choices=[(0, '< 2%'), (1, '2% tot 10%'), (2, '10% tot 30%'), (3, '30% tot 70%'), (4, '> 70%')])),
                ('intensiteit', models.IntegerField(choices=[(0, 'Laag'), (1, 'Midden'), (2, 'Hoog')])),
                ('conditiedeel', models.ForeignKey(to='onderhoud.Conditiedeel')),
            ],
            options={
                'verbose_name_plural': 'Gebreken',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gebrektype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=50)),
                ('ernst', models.IntegerField(choices=[(1, 'Gering'), (2, 'Serieus'), (3, 'Ernstig')])),
            ],
            options={
                'ordering': ['-ernst', 'naam'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hoofdcodering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('code', models.IntegerField()),
                ('naam', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Hoofdcoderingen',
                'ordering': ['code'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hoofdgroep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=50)),
                ('order', models.IntegerField()),
                ('standaard_elementen', models.ManyToManyField(blank=True, to='onderhoud.Element', null=True)),
            ],
            options={
                'verbose_name_plural': 'Hoofdgroepen',
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Maatregel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=80)),
                ('btw_percentage', models.FloatField()),
                ('ehprijs_excl', models.DecimalField(max_digits=8, decimal_places=2)),
                ('relatief', models.BooleanField(default=False)),
                ('hvh', models.FloatField(default=100)),
                ('start', models.PositiveIntegerField(default=2015)),
                ('cyclus', models.PositiveIntegerField(blank=True, null=True)),
                ('eind', models.PositiveIntegerField(blank=True, null=True)),
                ('opmerking', models.TextField(blank=True, null=True)),
                ('activiteit', models.ForeignKey(to='onderhoud.Activiteit')),
                ('deel', models.ForeignKey(to='onderhoud.Deel')),
            ],
            options={
                'verbose_name_plural': 'Maatregelen',
                'ordering': ['naam', 'start'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nengebrek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=60)),
                ('generiek', models.BooleanField(default=False)),
                ('gebrektype', models.ForeignKey(to='onderhoud.Gebrektype')),
            ],
            options={
                'verbose_name_plural': 'Nengebreken',
                'ordering': ['naam'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('naam', models.CharField(max_length=80)),
                ('start', models.IntegerField(default=2015)),
                ('complex', models.ForeignKey(to='onderhoud.Complex')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scenariogroep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('complexgroep', models.ForeignKey(to='onderhoud.Complexgroep')),
                ('scenario', models.ForeignKey(to='onderhoud.Scenario')),
            ],
            options={
                'verbose_name_plural': 'Scenariogroepen',
                'ordering': ['complexgroep'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gebrek',
            name='nengebrek',
            field=models.ForeignKey(to='onderhoud.Nengebrek'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='element',
            name='standaard_gebreken',
            field=models.ManyToManyField(blank=True, to='onderhoud.Nengebrek', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deel',
            name='scenariogroep',
            field=models.ForeignKey(to='onderhoud.Scenariogroep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiemeting',
            name='scenario',
            field=models.OneToOneField(blank=True, to='onderhoud.Scenario', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiegroep',
            name='conditiemeting',
            field=models.ForeignKey(to='onderhoud.Conditiemeting'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiegroep',
            name='scenariogroep',
            field=models.OneToOneField(blank=True, to='onderhoud.Scenariogroep', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiedeel',
            name='conditiegroep',
            field=models.ForeignKey(to='onderhoud.Conditiegroep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiedeel',
            name='deel',
            field=models.OneToOneField(blank=True, to='onderhoud.Deel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complexgroep',
            name='hoofdgroep',
            field=models.ForeignKey(to='onderhoud.Hoofdgroep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complexdeel',
            name='complexgroep',
            field=models.ForeignKey(to='onderhoud.Complexgroep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complexdeel',
            name='element',
            field=models.ForeignKey(to='onderhoud.Element'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complex',
            name='actueel_scenario',
            field=models.OneToOneField(blank=True, related_name='actueel', to='onderhoud.Scenario', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complex',
            name='admin',
            field=models.ForeignKey(blank=True, related_name='complexadmin', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='codering',
            name='hoofdcodering',
            field=models.ForeignKey(to='onderhoud.Hoofdcodering'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activiteitonderbouwing',
            name='deelactiviteit',
            field=models.ForeignKey(to='onderhoud.Deelactiviteit'),
            preserve_default=True,
        ),
    ]
