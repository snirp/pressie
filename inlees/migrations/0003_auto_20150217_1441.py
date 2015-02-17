# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inlees', '0002_auto_20150209_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importdeel',
            name='naam',
            field=models.CharField(max_length=130),
            preserve_default=True,
        ),
    ]
