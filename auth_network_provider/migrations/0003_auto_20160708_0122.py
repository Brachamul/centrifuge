# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-08 01:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth_network_provider', '0002_auto_20160705_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentials',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_network_provider.App'),
        ),
        migrations.AlterField(
            model_name='credentials',
            name='token',
            field=models.CharField(default=uuid.uuid4, max_length=32),
        ),
        migrations.AlterField(
            model_name='credentials',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, default='An Onymous', max_length=255, null=True, verbose_name='Prénom et Nom'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
