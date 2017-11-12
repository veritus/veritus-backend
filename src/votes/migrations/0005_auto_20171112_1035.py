# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-12 10:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0001_initial'),
        ('votes', '0004_auto_20171111_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='vote_record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='votes.VoteRecord'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('parliament_member', 'vote_record')]),
        ),
    ]
