# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inlees', '0003_auto_20150217_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importmaatregel',
            name='eh_prijs_excl',
            field=models.DecimalField(max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importmaatregel',
            name='eh_prijs_incl',
            field=models.DecimalField(max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
