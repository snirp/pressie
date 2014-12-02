# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hoofdcodering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('code', models.IntegerField()),
                ('naam', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='gebrektype',
            options={'ordering': ['-ernst', 'naam']},
        ),
        migrations.AlterModelOptions(
            name='nengebrek',
            options={'verbose_name_plural': 'Nengebreken', 'ordering': ['gebrektype', 'naam']},
        ),
        migrations.AddField(
            model_name='codering',
            name='hoofdcodering',
            field=models.ForeignKey(to='stam.Hoofdcodering', default=1),
            preserve_default=False,
        ),
    ]
