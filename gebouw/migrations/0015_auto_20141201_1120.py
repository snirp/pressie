# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0014_auto_20141130_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditiegroep',
            name='conditie',
            field=models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conditiedeel',
            name='conditiescore',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
