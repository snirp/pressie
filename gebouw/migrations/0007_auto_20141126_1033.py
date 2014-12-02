# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stam', '0005_hoofdgroep_standaard_elementen'),
        ('gebouw', '0006_auto_20141126_0954'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complexgroep',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('beschrijving', models.TextField(null=True, blank=True)),
                ('complex', models.ForeignKey(to='gebouw.Complex')),
                ('hoofdgroep', models.ForeignKey(to='stam.Hoofdgroep')),
            ],
            options={
                'verbose_name_plural': 'Complexgroepen',
                'ordering': ['hoofdgroep'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditiegroep',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('bevinding', models.TextField(null=True, blank=True)),
                ('conditiemeting', models.ForeignKey(to='gebouw.Conditiemeting')),
            ],
            options={
                'verbose_name_plural': 'Conditiegroepen',
                'ordering': ['scenariogroep'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scenariogroep',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('complexgroep', models.ForeignKey(to='gebouw.Complexgroep')),
                ('scenario', models.ForeignKey(to='gebouw.Scenario')),
            ],
            options={
                'verbose_name_plural': 'Scenariogroepen',
                'ordering': ['complexgroep'],
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='groep',
            name='complex',
        ),
        migrations.RemoveField(
            model_name='groep',
            name='hoofdgroep',
        ),
        migrations.AddField(
            model_name='conditiegroep',
            name='scenariogroep',
            field=models.OneToOneField(blank=True, to='gebouw.Scenariogroep', null=True),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='complexdeel',
            options={'verbose_name_plural': 'Complexdelen', 'ordering': ['complexgroep', 'element']},
        ),
        migrations.AlterModelOptions(
            name='deel',
            options={'verbose_name_plural': 'Delen', 'ordering': ['naam']},
        ),
        migrations.RemoveField(
            model_name='complexdeel',
            name='groep',
        ),
        migrations.RemoveField(
            model_name='conditiedeel',
            name='conditiemeting',
        ),
        migrations.RemoveField(
            model_name='conditiedeel',
            name='groep',
        ),
        migrations.RemoveField(
            model_name='deel',
            name='groep',
        ),
        migrations.DeleteModel(
            name='Groep',
        ),
        migrations.RemoveField(
            model_name='deel',
            name='scenario',
        ),
        migrations.RemoveField(
            model_name='deel',
            name='sort',
        ),
        migrations.AddField(
            model_name='complexdeel',
            name='complexgroep',
            field=models.ForeignKey(to='gebouw.Complexgroep', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conditiedeel',
            name='conditiegroep',
            field=models.ForeignKey(to='gebouw.Conditiegroep', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deel',
            name='scenariogroep',
            field=models.ForeignKey(to='gebouw.Scenariogroep', default=1),
            preserve_default=False,
        ),
    ]
