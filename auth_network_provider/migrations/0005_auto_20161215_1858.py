# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-15 18:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_network_provider', '0004_app_trusted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='username',
        ),
    ]