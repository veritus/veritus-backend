from django.db import models
from main.models import Entity
from politicians.models import Politician

class ParliamentMember(Politician):
    pass

class Parliament(Entity):
    start_date = models.DateField()
    end_date = models.DateField()
    parliament_members = models.ManyToManyField(ParliamentMember)

class ParliamentSession(Entity):
    session_number = models.IntegerField()
    parliament = models.ForeignKey(Parliament)
