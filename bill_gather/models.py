from __future__ import unicode_literals

from django.db import models

class Tag(models.Model):
    name = models.TextField()

class ParliamentSession(models.Model):
    session_number = models.IntegerField()


class Bill(models.Model):
    name = models.TextField()
    description_link = models.TextField()
    created_date = models.DateField(null=True)
    number = models.IntegerField(null=True)
    session = models.ForeignKey(ParliamentSession)

class BillTags(models.Model):
    bill = models.ForeignKey(Bill)
    tag = models.ForeignKey(Tag)