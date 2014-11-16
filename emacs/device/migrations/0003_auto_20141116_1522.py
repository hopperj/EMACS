# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0002_auto_20141115_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='humidity_control',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='device',
            name='pressure_control',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='device',
            name='tempature_control',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
