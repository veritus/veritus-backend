from __future__ import unicode_literals

from django.db import models
from bill_gather.models import Bill, Parliament

# Create your models here.

class Promise(models.Model):
    name = models.TextField()
    small_description = models.TextField()
    long_description = models.TextField()
    parliament_session = models.ForeignKey(Parliament)

class PromiseBill(models.Model):
    bill = models.ForeignKey(Bill)
    promise = models.ForeignKey(Promise)

    class Meta:
        # Dont want promise related to same tag multiple times
        unique_together = ('promise', 'bill',)

class SuggestedPromiseBill(models.Model):
    bill = models.ForeignKey(Bill)
    promise = models.ForeignKey(Promise)

    class Meta:
        # Dont want promise related to same tag multiple times
        unique_together = ('promise', 'bill',)