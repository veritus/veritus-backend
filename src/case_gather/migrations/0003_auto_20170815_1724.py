# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-15 17:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('case_gather', '0002_auto_20170815_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='parliament_session',
        ),
        migrations.DeleteModel(
            name='Bill',
        ),
    ]
