# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serverlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playertemp',
            name='server',
            field=models.ForeignKey(default=None, to='serverlist.Server'),
            preserve_default=True,
        ),
    ]
