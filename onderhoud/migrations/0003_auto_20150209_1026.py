# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onderhoud', '0002_auto_20150202_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='element',
            options={'ordering': ['naam'], 'verbose_name_plural': 'Elementen'},
        ),
        migrations.AddField(
            model_name='complex',
            name='bouwjaar',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complex',
            name='eenheden',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complex',
            name='huisnummer',
            field=models.CharField(max_length=20, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complex',
            name='plaats',
            field=models.CharField(max_length=60, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complex',
            name='straat',
            field=models.CharField(max_length=80, blank=True, null=True),
            preserve_default=True,
        ),
    ]
