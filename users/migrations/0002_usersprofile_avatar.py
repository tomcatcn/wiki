# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-11-07 23:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersprofile',
            name='avatar',
            field=models.ImageField(default='', upload_to='avatar', verbose_name='头像'),
        ),
    ]