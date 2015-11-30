# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serverlist', '0002_playertemp_server'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='Environment',
            field=models.CharField(default=b'Windows', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='game_name',
            field=models.CharField(default=b'Counter-Strike 1.6', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='mod',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='num_bots',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='password_protected',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='vac_secured',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='folder',
            field=models.CharField(default=b'None', max_length=200),
            preserve_default=True,
        ),
    ]
