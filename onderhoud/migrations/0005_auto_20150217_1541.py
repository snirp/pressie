# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onderhoud', '0004_auto_20150217_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deelactiviteit',
            name='eh_prijs',
            field=models.DecimalField(max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maatregel',
            name='ehprijs_excl',
            field=models.DecimalField(max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
