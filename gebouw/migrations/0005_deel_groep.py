# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0004_auto_20141126_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='deel',
            name='groep',
            field=models.ForeignKey(to='gebouw.Groep', blank=True, null=True),
            preserve_default=True,
        ),
    ]
