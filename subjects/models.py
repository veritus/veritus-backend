from django.db import models
from case_gather.models import Case
from promises.models import Promise
from main.models import Entity
from case_gather.models import Subject


class CaseSubject(Entity):
    case = models.ForeignKey(Case)
    subject = models.ForeignKey(Subject)

    class Meta:
        # Dont want case related to same tag multiple times
        unique_together = ('case', 'subject',)


class PromiseSubject(Entity):
    promise = models.ForeignKey(Promise)
    subject = models.ForeignKey(Subject)

    class Meta:
        # Dont want promise related to same tag multiple times
        unique_together = ('promise', 'subject',)