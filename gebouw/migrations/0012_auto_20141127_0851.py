# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0011_auto_20141126_2228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gebrek',
            name='ernst',
        ),
        migrations.AlterField(
            model_name='gebrek',
            name='nengebrek',
            field=models.ForeignKey(default=1, to='stam.Nengebrek'),
            preserve_default=False,
        ),
    ]
