from django.db import models
from main.models import Entity
from party.models import Party
from district.models import District

# Create your models here.
class Politician(Entity):
    party = models.ForeignKey(Party)
    initials = models.TextField()
    district = models.ForeignKey(District, related_name="politicians")
    districtNumber = models.IntegerField()
