# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gge_proxy_manager', '0002_botautologin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='product_key',
            field=models.CharField(unique=True, max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='alliance_rank',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playeralliancehistory',
            name='alliance_rank',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
