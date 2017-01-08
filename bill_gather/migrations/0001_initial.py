# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-08 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description_link', models.TextField()),
                ('althingi_created', models.DateField()),
                ('number', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Parliament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParliamentSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('session_number', models.IntegerField()),
                ('parliament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill_gather.Parliament')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bill',
            name='parliament_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill_gather.ParliamentSession'),
        ),
    ]
