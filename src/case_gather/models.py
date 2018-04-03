from django.db import models
from main.models import Entity
from parliament.models import ParliamentSession, ParliamentMember


class AlthingiStatusToStatusMapper(models.Model):
    althingi_status = models.TextField()
    status = models.TextField()


class Case(Entity):
    number = models.IntegerField()
    parliament_session = models.ForeignKey(ParliamentSession)
    case_type = models.TextField()
    althingi_status = models.TextField()
    althingi_link = models.TextField()
    status = models.TextField()

    class Meta:
        unique_together = ('parliament_session', 'number',)


class CaseCreator(Entity):
    parliament_member = models.ForeignKey(ParliamentMember)
    case = models.ForeignKey(Case, related_name='case_creators')

    class Meta:
        # Dont want promise related to same tag multiple times
        unique_together = ('parliament_member', 'case',)


class Subject(Entity):
    parliament_session = models.ForeignKey(
        ParliamentSession, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('Subject', null=True, blank=True)
