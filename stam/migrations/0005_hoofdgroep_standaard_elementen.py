# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stam', '0004_auto_20141125_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoofdgroep',
            name='standaard_elementen',
            field=models.ManyToManyField(blank=True, to='stam.Element', null=True),
            preserve_default=True,
        ),
    ]
