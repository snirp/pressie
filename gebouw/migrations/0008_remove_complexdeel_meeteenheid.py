# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gebouw', '0007_auto_20141126_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complexdeel',
            name='meeteenheid',
        ),
    ]
