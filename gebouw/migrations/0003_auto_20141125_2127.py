# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0002_auto_20141125_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complexdeel',
            name='meeteenheid',
            field=models.IntegerField(choices=[(1, '%'), (2, 'm'), (3, 'm2'), (5, 'st'), (6, 'won'), (7, 'vd')]),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='deel',
            unique_together=set([('naam', 'scenariogroep')]),
        ),
    ]
