''' Endpoints for promises '''
import logging
import django_filters

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Promise, PromiseCase, SuggestedPromiseCase
from .serializers import PromiseSerializerRead, PromiseSerializerWrite, PromiseCaseSerializer
from .serializers import SuggestedPromiseCaseSerializer

PROMISE_LOGGER = logging.getLogger('promise')

class PromiseFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Promise
        fields = {
            'parliament': ['exact'],
            'small_description': ['startswith', 'exact', 'contains'],
            }

class PromiseList(generics.ListAPIView):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializerRead
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PromiseFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        PROMISE_LOGGER.info(request.user)
        serializer = PromiseSerializerWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def promise_detail(request, promise_id):
    ''' Get by id, put and delete endpoints '''
    try:
        promise = Promise.objects.get(pk=promise_id)
    except Promise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        promise_read_serializer = PromiseSerializerRead(promise)
        return Response(promise_read_serializer.data)

    elif request.method == 'PUT':
        promise_write_serializer = PromiseSerializerWrite(promise, data=request.data)
        if promise_write_serializer.is_valid():
            promise_write_serializer.save()
            return Response(promise_write_serializer.data)
        return Response(promise_write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def promise_case_detail(request, promise_case_id):
    ''' Get by id endpoint '''
    try:
        promise_case = PromiseCase.objects.get(pk=promise_case_id)
    except Promise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PromiseCaseSerializer(promise_case)
        return Response(serializer.data)


class SuggestedPromiseCaseFilter(django_filters.rest_framework.FilterSet):
    ''' filter for suggested promise case connections '''
    class Meta:
        model = SuggestedPromiseCase
        fields = ['case', 'promise']


class SuggestedPromiseCaseList(generics.ListAPIView):
    ''' SuggestedPromiseCaseList endpoint '''
    queryset = SuggestedPromiseCase.objects.all()
    serializer_class = SuggestedPromiseCaseSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = SuggestedPromiseCaseFilter


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def suggested_promise_case_detail(request, suggested_promise_id):
    ''' Get all suggested promise case '''
    try:
        suggested_promise_case = SuggestedPromiseCase.objects.get(pk=suggested_promise_id)
    except Promise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SuggestedPromiseCaseSerializer(suggested_promise_case)
        return Response(serializer.data)
