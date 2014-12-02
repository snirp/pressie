# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complex',
            name='actueel_scenario',
            field=models.OneToOneField(blank=True, null=True, related_name='actueel', to='gebouw.Scenario'),
            preserve_default=True,
        ),
    ]
