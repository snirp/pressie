# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stam', '0003_auto_20141125_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='eenheid',
            field=models.IntegerField(choices=[(1, '%'), (2, 'm'), (3, 'm2'), (5, 'st'), (6, 'won'), (7, 'vd')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='element',
            name='standaard_activiteiten',
            field=models.ManyToManyField(blank=True, to='stam.Activiteit', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='element',
            name='standaard_gebreken',
            field=models.ManyToManyField(blank=True, to='stam.Nengebrek', null=True),
            preserve_default=True,
        ),
    ]
