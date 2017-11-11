# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-11 16:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('politicians', '0002_auto_20171111_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='politician',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='politicians', to='district.District'),
        ),
        migrations.AlterField(
            model_name='politician',
            name='districtNumber',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='politician',
            name='initials',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='politician',
            name='party',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Party'),
        ),
    ]