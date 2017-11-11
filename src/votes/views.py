import django_filters

from rest_framework import generics
from .models import Vote, VoteRecord
from .serializers import VoteSerializer, VoteRecordSerializer

class VoteRecordList(generics.ListAPIView):
    '''
    get:
        Get a list of all vote records.
    '''
    queryset = VoteRecord.objects.all()
    serializer_class = VoteRecordSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('case',)

class VoteList(generics.ListAPIView):
    '''
    get:
        Get a list of all votes.
    '''
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('vote_record',)
