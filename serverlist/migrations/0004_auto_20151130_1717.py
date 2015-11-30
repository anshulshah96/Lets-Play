# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serverlist', '0003_auto_20151130_1625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='Environment',
            new_name='environment',
        ),
        migrations.AddField(
            model_name='server',
            name='protocol',
            field=models.CharField(default=b'None', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='response_header',
            field=models.CharField(default=b'None', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='server_type',
            field=models.CharField(default=b'None', max_length=200),
            preserve_default=True,
        ),
    ]
