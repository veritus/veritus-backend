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

class SuperSubject(Entity):
    parliament_session = models.ForeignKey(ParliamentSession, null=True, blank=True)
    supersubject_id = models.IntegerField(null=True, blank=True)


class Subject(Entity):
    parliament_session = models.ForeignKey(ParliamentSession, null=True, blank=True)
    subject_id = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    supersubject = models.ForeignKey(SuperSubject, null=True, blank=True)


