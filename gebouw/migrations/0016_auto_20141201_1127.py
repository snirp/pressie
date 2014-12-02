# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0015_auto_20141201_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complex',
            name='foto',
            field=models.ImageField(upload_to='complex', blank=True, null=True),
            preserve_default=True,
        ),
    ]
