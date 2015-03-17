# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gge_proxy_manager', '0004_auto_20150208_1837'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='castle',
            index_together=set([('kingdom', 'pos_x', 'pos_y'), ('game', 'type', 'player')]),
        ),
    ]
