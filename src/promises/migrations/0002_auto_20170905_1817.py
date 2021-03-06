# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-05 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='suggestedpromisecase',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='suggestedpromisecase',
            name='case',
        ),
        migrations.RemoveField(
            model_name='suggestedpromisecase',
            name='promise',
        ),
        migrations.AddField(
            model_name='promisecase',
            name='percent_of_related_subjects',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='promisecase',
            name='relationship_type',
            field=models.CharField(
                choices=[('C', 'Connected'), ('S', 'Suggested')], default='C', max_length=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SuggestedPromiseCase',
        ),
    ]
