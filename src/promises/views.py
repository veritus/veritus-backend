''' Endpoints for promises '''
import django_filters

from rest_framework import generics
from .models import Promise, PromiseCase
from .serializers import PromiseSerializer, PromiseCaseSerializer


class PromiseFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Promise
        fields = {
            'parliament': ['exact'],
            'small_description': ['startswith', 'exact', 'contains'],
        }


class PromiseList(generics.ListCreateAPIView):
    '''
    get:
        Get a list of all promises.

    post:
        Add new promise.
    '''
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PromiseFilter


class PromiseDetails(generics.RetrieveUpdateAPIView):
    '''
    get:
        Get promise by id

    put / patch:
        Update a promise.
    '''
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer


class PromiseCaseFilter(django_filters.rest_framework.FilterSet):
    ''' filter for promise case '''
    class Meta:
        model = PromiseCase
        fields = ['case', 'promise']


class PromiseCaseList(generics.ListAPIView):
    ''' PromiseCaseList endpoint '''
    queryset = PromiseCase.objects.all()
    serializer_class = PromiseCaseSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PromiseCaseFilter


class PromiseCaseDetails(generics.RetrieveAPIView):
    queryset = PromiseCase.objects.all()
    serializer_class = PromiseCaseSerializer
