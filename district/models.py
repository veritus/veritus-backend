from django.db import models
from main.models import Entity

class District(Entity):
    abbreviation = models.TextField()