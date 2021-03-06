# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-05 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('case_gather', '0003_auto_20170815_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteRecord',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('althingi_id', models.IntegerField()),
                ('yes', models.IntegerField(blank=True, null=True)),
                ('no', models.IntegerField(blank=True, null=True)),
                ('didNotVote', models.IntegerField(blank=True, null=True)),
                ('althingi_result', models.TextField(blank=True, null=True)),
                ('case', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='case_gather.Case')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
