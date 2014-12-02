# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stam', '0005_hoofdgroep_standaard_elementen'),
        ('gebouw', '0003_auto_20141125_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groep',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('beschrijving', models.TextField(null=True, blank=True)),
                ('complex', models.ForeignKey(to='gebouw.Complex')),
                ('hoofdgroep', models.ForeignKey(to='stam.Hoofdgroep')),
            ],
            options={
                'ordering': ['hoofdgroep'],
                'verbose_name_plural': 'Groepen',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='complexgroep',
            name='complex',
        ),
        migrations.RemoveField(
            model_name='complexgroep',
            name='hoofdgroep',
        ),
        migrations.RemoveField(
            model_name='conditiegroep',
            name='conditiemeting',
        ),
        migrations.RemoveField(
            model_name='conditiegroep',
            name='scenariogroep',
        ),
        migrations.RemoveField(
            model_name='scenariogroep',
            name='complexgroep',
        ),
        migrations.RemoveField(
            model_name='scenariogroep',
            name='scenario',
        ),
        migrations.AlterModelOptions(
            name='complexdeel',
            options={'ordering': ['groep', 'element'], 'verbose_name_plural': 'Complexdelen'},
        ),
        migrations.AlterModelOptions(
            name='deel',
            options={'ordering': ['sort', 'naam'], 'verbose_name_plural': 'Delen'},
        ),
        migrations.RemoveField(
            model_name='complexdeel',
            name='complexgroep',
        ),
        migrations.AlterUniqueTogether(
            name='deel',
            unique_together=set([]),
        ),
        migrations.DeleteModel(
            name='Complexgroep',
        ),
        migrations.RemoveField(
            model_name='conditiedeel',
            name='conditiegroep',
        ),
        migrations.DeleteModel(
            name='Conditiegroep',
        ),
        migrations.RemoveField(
            model_name='deel',
            name='scenariogroep',
        ),
        migrations.DeleteModel(
            name='Scenariogroep',
        ),
        migrations.AddField(
            model_name='complexdeel',
            name='groep',
            field=models.ForeignKey(to='gebouw.Groep', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditiedeel',
            name='groep',
            field=models.ForeignKey(to='gebouw.Groep', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deel',
            name='sort',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
