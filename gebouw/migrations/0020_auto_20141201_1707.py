# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0019_auto_20141201_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditiedeel',
            name='conditiescore',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]),
            preserve_default=True,
        ),
    ]
