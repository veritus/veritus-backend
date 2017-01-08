from __future__ import unicode_literals

from django.db import models
from bill_gather.models import Bill
from promises.models import Promise


# Create your models here.
class Tag(models.Model):
    name = models.TextField()


class BillTags(models.Model):
    bill = models.ForeignKey(Bill)
    tag = models.ForeignKey(Tag)

    class Meta:
        # Dont want bill related to same tag multiple times
        unique_together = ('bill', 'tag',)


class PromiseTags(models.Model):
    promise = models.ForeignKey(Promise)
    tag = models.ForeignKey(Tag)

    class Meta:
        # Dont want promise related to same tag multiple times
        unique_together = ('promise', 'tag',)