# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gge_proxy_manager', '0006_auto_20150209_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='castle',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
            preserve_default=True,
        ),
    ]
