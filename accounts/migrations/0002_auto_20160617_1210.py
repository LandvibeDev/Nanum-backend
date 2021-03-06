# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 12:10
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nanumuser',
            name='birthday',
            field=models.DateField(blank=True, help_text='생일'),
        ),
        migrations.AlterField(
            model_name='nanumuser',
            name='profile_image',
            field=models.ImageField(blank=True, help_text='프로필 사진', null=True, upload_to=accounts.models.get_file_path),
        ),
    ]
