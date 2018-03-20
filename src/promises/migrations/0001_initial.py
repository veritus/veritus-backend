# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-11 18:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parliament', '0001_initial'),
        ('politicians', '0001_initial'),
        ('case_gather', '0001_initial'),
        ('party', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promise',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('fulfilled', models.BooleanField(default=False)),
                ('small_description', models.TextField()),
                ('long_description', models.TextField()),
                ('parliament', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='parliament.Parliament')),
                ('party', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Party')),
                ('politician', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                 related_name='promises', to='politicians.Politician')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PromiseCase',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('case', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='case_gather.Case')),
                ('promise', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='promises.Promise')),
            ],
        ),
        migrations.CreateModel(
            name='SuggestedPromiseCase',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('case', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='case_gather.Case')),
                ('promise', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='promises.Promise')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='suggestedpromisecase',
            unique_together=set([('promise', 'case')]),
        ),
        migrations.AlterUniqueTogether(
            name='promisecase',
            unique_together=set([('promise', 'case')]),
        ),
    ]
