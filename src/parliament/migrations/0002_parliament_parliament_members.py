# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-12 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parliament',
            name='parliament_members',
            field=models.ManyToManyField(to='parliament.ParliamentMember'),
        ),
    ]
