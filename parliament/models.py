from django.db import models
from main.models import Entity
from party.models import Party
from district.models import District

class Parliament(Entity):
    start_date = models.DateField()
    end_date = models.DateField()


class ParliamentSession(Entity):
    session_number = models.IntegerField()
    parliament = models.ForeignKey(Parliament)

class ParliamentMember(Entity):
    party = models.ForeignKey(Party)
    initials = models.TextField()
    district = models.ForeignKey(District)
    districtNumber = models.IntegerField()
