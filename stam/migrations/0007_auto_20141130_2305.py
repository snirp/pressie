# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stam', '0006_activiteit_eenheid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nengebrek',
            options={'ordering': ['naam'], 'verbose_name_plural': 'Nengebreken'},
        ),
    ]
