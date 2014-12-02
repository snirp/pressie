# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0017_auto_20141201_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditiedeel',
            name='conditiescore',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
