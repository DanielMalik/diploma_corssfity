# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crossfity', '0004_auto_20170128_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='sms_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]