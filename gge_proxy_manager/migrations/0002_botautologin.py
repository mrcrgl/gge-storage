# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gge_proxy_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotAutoLogin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('from_hour', models.PositiveSmallIntegerField(default=0)),
                ('to_hour', models.PositiveSmallIntegerField(default=24)),
                ('enabled', models.BooleanField(default=True)),
                ('player', models.OneToOneField(related_name='bot_auto_login', to='gge_proxy_manager.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
