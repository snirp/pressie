# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stam', '0002_auto_20141125_1335'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hoofdcodering',
            options={'ordering': ['code'], 'verbose_name_plural': 'Hoofdcoderingen'},
        ),
        migrations.AddField(
            model_name='element',
            name='eenheid',
            field=models.IntegerField(default=1, choices=[(1, '%'), (2, 'm'), (3, 'm2'), (5, 'st')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='element',
            name='omschrijving',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='element',
            name='standaard_activiteiten',
            field=models.ManyToManyField(to='stam.Activiteit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='element',
            name='standaard_gebreken',
            field=models.ManyToManyField(to='stam.Nengebrek'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='element',
            name='steekwoorden',
            field=models.CharField(max_length=100, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='element',
            name='vervangwaarde',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
