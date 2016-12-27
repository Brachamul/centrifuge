# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 20:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_network_provider', '0003_auto_20161227_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentials',
            name='last_token_refresh',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='networkuser',
            name='last_verification',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]