from django.db import models

from main.models import Entity
from case_gather.models import Case
from parliament.models import ParliamentMember

class VoteRecord(Entity):
    '''
    The voting record of each case
    '''
    case = models.ForeignKey(Case)
    althingi_id = models.IntegerField()
    '''
    Number of people who voted yes
    '''
    yes = models.IntegerField(null=True, blank=True)
    '''
    Number of people who voted no
    '''
    no = models.IntegerField(null=True, blank=True)
    '''
    Number of people who did not vote
    '''
    didNotVote = models.IntegerField(null=True, blank=True)
    '''
    The result of the vote according to althingi
    '''
    althingi_result = models.TextField(null=True, blank=True)

class Vote(Entity):
    parliament_member = models.ForeignKey(ParliamentMember)
    althingi_result = models.TextField()
