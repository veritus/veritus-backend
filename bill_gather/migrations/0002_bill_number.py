# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_gather', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]
