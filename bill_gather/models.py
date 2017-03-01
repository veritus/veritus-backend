from django.db import models
from main.models import Entity
from parliament.models import ParliamentSession


class Bill(Entity):
    description_link = models.TextField()
    althingi_created = models.DateField()
    number = models.IntegerField()
    parliament_session = models.ForeignKey(ParliamentSession)

