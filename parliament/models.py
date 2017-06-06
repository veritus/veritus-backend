from django.db import models
from main.models import Entity
from politicians.models import Politician

class Parliament(Entity):
    start_date = models.DateField()
    end_date = models.DateField()


class ParliamentSession(Entity):
    session_number = models.IntegerField()
    parliament = models.ForeignKey(Parliament)

class ParliamentMember(Politician):
    pass