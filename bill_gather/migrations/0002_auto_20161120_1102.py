# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 11:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bill_gather', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='billtags',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='billtags',
            name='bill',
        ),
        migrations.RemoveField(
            model_name='billtags',
            name='tag',
        ),
        migrations.DeleteModel(
            name='BillTags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
