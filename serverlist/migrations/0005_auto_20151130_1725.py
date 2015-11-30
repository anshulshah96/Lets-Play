# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serverlist', '0004_auto_20151130_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='password_protected',
            field=models.CharField(default=b'No', max_length=10),
            preserve_default=True,
        ),
    ]
