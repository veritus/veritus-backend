from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Promise, PromiseCase, SuggestedPromiseCase
from .serializers import PromiseSerializerRead, PromiseSerializerWrite, PromiseCaseSerializer, SuggestedPromiseCaseSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import django_filters
import logging
from rest_framework import generics


promise_logger = logging.getLogger('promise')

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
        promise_logger.info(request.user)
        serializer = PromiseSerializerWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticatedOrReadOnly,))
#def promise_list(request):
#    if request.method == 'GET':
#        promises = Promise.objects.all()
#        serializer = PromiseSerializerRead(promises, many=True)
#        return Response(serializer.data)
#    elif request.method == 'POST':
#        promise_logger.info(request.user)
#        serializer = PromiseSerializerWrite(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def promise_detail(request, pk):
    try:
        promise = Promise.objects.get(pk=pk)
    except Promise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PromiseSerializerRead(promise)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PromiseSerializerWrite(promise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        promise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PromiseCaseFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = PromiseCase
        fields = ['case', 'promise']


class PromiseCaseList(generics.ListAPIView):
    queryset = PromiseCase.objects.all()
    serializer_class = PromiseCaseSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PromiseCaseFilter


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def promise_case_detail(request, pk):

    try:
        promise_case = PromiseCase.objects.get(pk=pk)
    except Promise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PromiseCaseSerializer(promise_case)
        return Response(serializer.data)


class SuggestedPromiseCaseFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = SuggestedPromiseCase
        fields = ['case', 'promise']


class SuggestedPromiseCaseList(generics.ListAPIView):
    queryset = SuggestedPromiseCase.objects.all()
    serializer_class = SuggestedPromiseCaseSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = SuggestedPromiseCaseFilter


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def suggested_promise_case_detail(request, pk):

    try:
        suggested_promise_case = SuggestedPromiseCase.objects.get(pk=pk)
    except Promise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SuggestedPromiseCaseSerializer(suggested_promise_case)
        return Response(serializer.data)
