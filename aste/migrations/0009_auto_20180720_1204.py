# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-20 10:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aste', '0008_auto_20180705_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]