from __future__ import unicode_literals

from django.db import models
from bill_gather.models import Bill
from parliament.models import Parliament
from main.models import Entity


class Promise(Entity):
    small_description = models.TextField()
    long_description = models.TextField()
    parliament = models.ForeignKey(Parliament)


class PromiseBill(Entity):
    bill = models.ForeignKey(Bill)
    promise = models.ForeignKey(Promise)

    class Meta:
        # Dont want promise related to same tag multiple times
        unique_together = ('promise', 'bill',)


class SuggestedPromiseBill(Entity):
    bill = models.ForeignKey(Bill)
    promise = models.ForeignKey(Promise)

    class Meta:
        # Dont want promise related to same tag multiple times
        unique_together = ('promise', 'bill',)