from django.db import models
from case_gather.models import Case
from parliament.models import Parliament
from politicians.models import Politician
from party.models import Party
from main.models import Entity


class Promise(Entity):
    fulfilled = models.BooleanField(default=False)
    small_description = models.TextField()
    long_description = models.TextField()
    parliament = models.ForeignKey(Parliament)
    politician = models.ForeignKey(Politician, null=True, related_name='promises')
    party = models.ForeignKey(Party, null=True)


RELATIONSHIP_TYPES = (
    ('C', 'Connected'),
    ('S', 'Suggested'),
)

class PromiseCase(Entity):
    case = models.ForeignKey(Case)
    promise = models.ForeignKey(Promise)
    relationship_type = models.CharField(max_length=1, choices=RELATIONSHIP_TYPES)
    percent_of_related_subjects = models.IntegerField()

    class Meta:
        # Dont want promise related to same tag multiple times
        unique_together = ('promise', 'case',)

