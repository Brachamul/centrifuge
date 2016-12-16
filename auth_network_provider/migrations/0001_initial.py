# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-16 23:26
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, max_length=254, unique=True, verbose_name='Courriel')),
                ('name', models.CharField(blank=True, default='An Onymous', max_length=255, null=True, verbose_name='Prénom et Nom')),
                ('is_staff', models.BooleanField(default=False, help_text="Précise si l'utilisateur peut se connecter à ce site d'administration.", verbose_name='Staff Status')),
                ('is_active', models.BooleanField(default=True, help_text="Précise si l'utilisateur doit être considéré comme actif. Décochez ceci plutôt que de supprimer le compte.", verbose_name='Active')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
            ],
            options={
                'verbose_name_plural': 'Users',
                'verbose_name': 'Utilisateur',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('trusted', models.BooleanField(default=False)),
                ('secret', models.CharField(default=uuid.uuid4, editable=False, max_length=32)),
                ('set_token_url', models.CharField(help_text='eg: http://localhost:8008/auth/set-token/', max_length=5000)),
                ('callback_url', models.CharField(help_text='eg: http://localhost:8008/auth/callback/', max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=uuid.uuid4, max_length=32)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_network_provider.App')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Credentials',
                'verbose_name': 'Credentials',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='apps',
            field=models.ManyToManyField(through='auth_network_provider.Credentials', to='auth_network_provider.App'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
