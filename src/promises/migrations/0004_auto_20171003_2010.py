# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-03 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '0003_auto_20171003_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promisecase',
            name='relationship_type',
            field=models.CharField(
                choices=[('C', 'Connected'), ('S', 'Suggested')], max_length=3),
        ),
    ]
