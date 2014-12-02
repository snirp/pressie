# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0005_deel_groep'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditiedeel',
            name='conditiemeting',
            field=models.ForeignKey(to='gebouw.Conditiemeting', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deel',
            name='scenario',
            field=models.ForeignKey(to='gebouw.Scenario', default=1),
            preserve_default=False,
        ),
    ]
