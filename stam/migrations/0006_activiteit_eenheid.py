# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stam', '0005_hoofdgroep_standaard_elementen'),
    ]

    operations = [
        migrations.AddField(
            model_name='activiteit',
            name='eenheid',
            field=models.IntegerField(choices=[(1, '%'), (2, 'm'), (3, 'm2'), (5, 'st'), (6, 'won'), (7, 'vd')], default=1),
            preserve_default=False,
        ),
    ]
