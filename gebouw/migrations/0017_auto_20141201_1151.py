# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0016_auto_20141201_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditiegroep',
            name='conditie',
            field=models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]),
            preserve_default=True,
        ),
    ]
