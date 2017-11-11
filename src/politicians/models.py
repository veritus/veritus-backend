from django.db import models
from main.models import Entity
from party.models import Party
from district.models import District

class Politician(Entity):
    party = models.ForeignKey(Party, null=True)
    initials = models.TextField(null=True)
    district = models.ForeignKey(District, related_name="politicians", null=True)
    districtNumber = models.IntegerField(null=True)
