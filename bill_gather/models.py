from __future__ import unicode_literals

from django.db import models


class Bill(models.Model):
    name = models.TextField()
    description = models.TextField()