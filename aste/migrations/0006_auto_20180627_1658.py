# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-27 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aste', '0005_puntata_utente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='foto',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]
