# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-24 22:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_network_provider', '0004_app_trusted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='new_token_url',
            new_name='set_token_url',
        ),
    ]
