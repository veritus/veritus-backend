""" Webservice endpoints for cases """
import django_filters
from rest_framework import generics
from .models import Case
from .serializers import CaseSerializer

class CaseFilter(django_filters.rest_framework.FilterSet):
    ''' filter for cases '''
    class Meta:
        model = Case
        fields = [
            'parliament_session',
            'case_type',
            'status',
            'althingi_status',
        ]

class CaseList(generics.ListAPIView):
    ''' PromiseCaseList endpoint '''
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = CaseFilter

class CaseDetails(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

