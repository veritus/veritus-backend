# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-11 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0002_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='vote_record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='votes.VoteRecord'),
        ),
    ]