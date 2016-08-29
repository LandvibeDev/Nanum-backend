# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-29 08:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('study', '0001_initial'),
        ('reference', '0001_initial'),
        ('accounts', '0004_auto_20160709_0430'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='board',
            field=models.ForeignKey(blank=True, help_text='참고자료와 관련된 게시판', null=True, on_delete=django.db.models.deletion.CASCADE, to='study.Board'),
        ),
        migrations.AddField(
            model_name='reference',
            name='user',
            field=models.ForeignKey(blank=True, help_text='참고자료를 업로드한 사용자', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.NanumUser'),
        ),
    ]
