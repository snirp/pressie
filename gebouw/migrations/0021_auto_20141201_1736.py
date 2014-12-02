# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0020_auto_20141201_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maatregel',
            old_name='percentage',
            new_name='relatief',
        ),
    ]
