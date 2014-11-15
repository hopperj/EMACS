# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0002_auto_20141115_0250'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('measure', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=64)),
                ('device', models.ForeignKey(to='device.Device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
