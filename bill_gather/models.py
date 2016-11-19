from __future__ import unicode_literals

from django.db import models


class ParliamentSession(models.Model):
    session_number = models.IntegerField()


class Bill(models.Model):
    name = models.TextField()
    description = models.TextField()
    created_date = models.DateField(null=True)
    number = models.IntegerField(null=True)
    session = models.ForeignKey(ParliamentSession)

