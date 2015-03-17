# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import lib.messaging.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(unique=True, max_length=128, db_index=True)),
                ('title', models.CharField(max_length=64)),
                ('subject', models.CharField(max_length=64)),
                ('always_bcc_to', models.EmailField(default=None, max_length=75, null=True, blank=True)),
                ('template', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemplateAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(default=None, max_length=64, null=True, blank=True)),
                ('file', models.FileField(upload_to=lib.messaging.models.upload_attachment)),
                ('template', models.ForeignKey(related_name='attachments', to='messaging.Template')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
