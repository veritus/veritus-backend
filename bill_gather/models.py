from __future__ import unicode_literals
from django.db import models


class Parliament(models.Model):
    name = models.TextField()


class ParliamentSession(models.Model):
    session_number = models.IntegerField()
    parliament = models.ForeignKey(Parliament)


class Bill(models.Model):
    name = models.TextField()
    description_link = models.TextField()
    created_date = models.DateField()
    number = models.IntegerField()
    parliament_session = models.ForeignKey(ParliamentSession)

