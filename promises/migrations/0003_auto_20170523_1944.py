# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-23 19:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '0002_auto_20170523_1933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promise',
            old_name='parliamentMember',
            new_name='parliament_member',
        ),
    ]