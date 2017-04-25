from __future__ import unicode_literals
from main.models import Entity

from django.db import models

class Party(Entity):
    website = models.TextField()
