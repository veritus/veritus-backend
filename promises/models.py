from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Promise(models.Model):
    name = models.TextField()
    small_description = models.TextField()
    long_description = models.TextField()