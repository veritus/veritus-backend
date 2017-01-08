from __future__ import unicode_literals
from django.db import models
from main.models import Entity


class Parliament(Entity):
    start_date = models.DateField()
    end_date = models.DateField()


class ParliamentSession(Entity):
    session_number = models.IntegerField()
    parliament = models.ForeignKey(Parliament)


class Bill(Entity):
    description_link = models.TextField()
    althingi_created = models.DateField()
    number = models.IntegerField()
    parliament_session = models.ForeignKey(ParliamentSession)

