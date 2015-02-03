# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onderhoud', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deel',
            name='scenariogroep',
            field=models.ForeignKey(to='onderhoud.Scenariogroep', related_name='delen'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maatregel',
            name='deel',
            field=models.ForeignKey(to='onderhoud.Deel', related_name='maatregelen'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maatregel',
            name='start',
            field=models.PositiveIntegerField(default=2016),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scenario',
            name='start',
            field=models.IntegerField(default=2016),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scenariogroep',
            name='scenario',
            field=models.ForeignKey(to='onderhoud.Scenario', related_name='scenariogroepen'),
            preserve_default=True,
        ),
    ]
