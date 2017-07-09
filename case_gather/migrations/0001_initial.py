# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-06 19:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parliament', '0001_initial'),
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
                ('parliament_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parliament.ParliamentSession')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField()),
                ('case_type', models.TextField()),
                ('case_status', models.TextField()),
                ('parliament_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parliament.ParliamentSession')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='case_gather.Subject')),
                ('parliament_session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parliament.ParliamentSession')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
