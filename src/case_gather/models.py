from django.db import models
from main.models import Entity
from parliament.models import ParliamentSession


class Bill(Entity):
    description_link = models.TextField()
    althingi_created = models.DateField()
    number = models.IntegerField()
    parliament_session = models.ForeignKey(ParliamentSession)


class Case(Entity):
    number = models.IntegerField()
    parliament_session = models.ForeignKey(ParliamentSession)
    case_type = models.TextField()
    case_status = models.TextField()


class Subject(Entity):
    parliament_session = models.ForeignKey(ParliamentSession, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('Subject', null=True, blank=True)