# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0010_maatregel_deel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maatregel',
            name='uitvoer_percentage',
        ),
        migrations.AddField(
            model_name='maatregel',
            name='hvh',
            field=models.FloatField(default=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maatregel',
            name='percentage',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maatregel',
            name='activiteit',
            field=models.ForeignKey(default=1, to='stam.Activiteit'),
            preserve_default=False,
        ),
    ]
