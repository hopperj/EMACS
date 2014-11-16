# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_auto_20141116_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='tempature_control',
        ),
    ]
