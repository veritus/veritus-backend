# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-28 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('promises', '0001_initial'),
        ('case_gather', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case_gather.Case')),
            ],
        ),
        migrations.CreateModel(
            name='PromiseTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promises.Promise')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='promisetags',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.Tag'),
        ),
        migrations.AddField(
            model_name='casetags',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='promisetags',
            unique_together=set([('promise', 'tag')]),
        ),
        migrations.AlterUniqueTogether(
            name='casetags',
            unique_together=set([('case', 'tag')]),
        ),
    ]