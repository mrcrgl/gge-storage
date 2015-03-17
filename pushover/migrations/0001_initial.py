# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gge_proxy_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_token', models.CharField(max_length=128)),
                ('enabled', models.BooleanField(default=True)),
                ('user', models.OneToOneField(related_name='pushover_client', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match_my_players', models.BooleanField(default=False, db_index=True)),
                ('priority', models.SmallIntegerField(default=0, choices=[(-2, b'Stumm'), (-1, b'Ruhig'), (0, b'Normal'), (1, b'Wichtig'), (2, b'Emergency')])),
                ('retry', models.PositiveIntegerField(default=30)),
                ('expire', models.PositiveIntegerField(default=300)),
                ('client', models.ForeignKey(related_name='notifications', to='pushover.Client')),
                ('match_alliance', models.ForeignKey(default=None, blank=True, to='gge_proxy_manager.Alliance', null=True)),
            ],
            options={
                'ordering': ('-priority',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotifyVillage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match_ruin', models.BooleanField(default=False)),
                ('match_unassigned', models.BooleanField(default=False)),
                ('priority', models.SmallIntegerField(default=0, choices=[(-2, b'Stumm'), (-1, b'Ruhig'), (0, b'Normal'), (1, b'Wichtig'), (2, b'Emergency')])),
                ('retry', models.PositiveIntegerField(default=30)),
                ('expire', models.PositiveIntegerField(default=300)),
                ('client', models.ForeignKey(related_name='village_notifications', to='pushover.Client')),
                ('kingdom', models.ForeignKey(default=None, to='gge_proxy_manager.Kingdom', null=True)),
            ],
            options={
                'ordering': ('-priority',),
            },
            bases=(models.Model,),
        ),
    ]
