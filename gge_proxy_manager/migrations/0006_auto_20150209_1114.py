# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gge_proxy_manager', '0005_auto_20150209_1110'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='castle',
            index_together=set([('kingdom', 'pos_x', 'pos_y'), ('game', 'type', 'player', 'updated')]),
        ),
    ]
