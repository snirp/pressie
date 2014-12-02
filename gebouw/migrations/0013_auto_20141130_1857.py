# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0012_auto_20141127_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditiefoto',
            name='foto_link',
            field=models.ImageField(upload_to='images'),
            preserve_default=True,
        ),
    ]
