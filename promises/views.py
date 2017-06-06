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


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def promise_list(request):
    ''' Get all and post endpoints '''
    if request.method == 'GET':
        promises = Promise.objects.all()
        read_serializer = PromiseSerializerRead(promises, many=True)
        return Response(read_serializer.data)
    elif request.method == 'POST':
        PROMISE_LOGGER.info(request.user)
        write_serializer = PromiseSerializerWrite(data=request.data)
        if write_serializer.is_valid():
            write_serializer.save()
            return Response(write_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def promise_detail(request, promise_id):
    ''' Get by id, put and delete endpoints '''
    try:
        promise = Promise.objects.get(pk=promise_id)
    except Promise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        read_serializer = PromiseSerializerRead(promise)
        return Response(read_serializer.data)

    elif request.method == 'PUT':
        write_serializer = PromiseSerializerWrite(promise, data=request.data)
        if write_serializer.is_valid():
            write_serializer.save()
            return Response(write_serializer.data)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
