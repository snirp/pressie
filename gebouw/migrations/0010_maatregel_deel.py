# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0009_auto_20141126_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='maatregel',
            name='deel',
            field=models.ForeignKey(to='gebouw.Deel', default=1),
            preserve_default=False,
        ),
    ]
