# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0013_auto_20141130_1857'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deel',
            options={'verbose_name_plural': 'Delen', 'ordering': ['scenariogroep', 'naam']},
        ),
        migrations.RenameField(
            model_name='conditiefoto',
            old_name='foto_link',
            new_name='foto',
        ),
    ]
