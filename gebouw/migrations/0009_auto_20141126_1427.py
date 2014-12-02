# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0008_remove_complexdeel_meeteenheid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maatregel',
            name='activiteit',
            field=models.ForeignKey(to='stam.Activiteit', blank=True, null=True),
            preserve_default=True,
        ),
    ]
