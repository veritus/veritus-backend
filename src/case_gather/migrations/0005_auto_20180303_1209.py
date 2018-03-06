# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-03-03 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0002_parliament_parliament_members'),
        ('case_gather', '0004_auto_20171111_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='number',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='case',
            unique_together=set([('parliament_session', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='casecreator',
            unique_together=set([('parliament_member', 'case')]),
        ),
    ]