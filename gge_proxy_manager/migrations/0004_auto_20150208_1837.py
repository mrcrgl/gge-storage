# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gge_proxy_manager', '0003_auto_20150129_0927'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='mapexplorer',
            index_together=set([('active', 'kingdom')]),
        ),
    ]
