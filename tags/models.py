from django.db import models
from case_gather.models import Case
from promises.models import Promise


# Create your models here.
class Tag(models.Model):
    name = models.TextField()


class CaseTags(models.Model):
    case = models.ForeignKey(Case)
    tag = models.ForeignKey(Tag)

    class Meta:
        # Dont want case related to same tag multiple times
        unique_together = ('case', 'tag',)


class PromiseTags(models.Model):
    promise = models.ForeignKey(Promise)
    tag = models.ForeignKey(Tag)

    class Meta:
        # Dont want promise related to same tag multiple times
        unique_together = ('promise', 'tag',)