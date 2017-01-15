from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Promise, PromiseBill, SuggestedPromiseBill
from .serializers import PromiseSerializerRead, PromiseSerializerWrite, PromiseBillSerializer, SuggestedPromiseBillSerializer
from rest_framework import permissions
import django_filters
from rest_framework import generics

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def promise_list(request):

    if request.method == 'GET':
        promises = Promise.objects.all()
        serializer = PromiseSerializerRead(promises, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PromiseSerializerWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
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


class PromiseBillFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = PromiseBill
        fields = ['bill', 'promise']


class PromiseBillList(generics.ListAPIView):
    queryset = PromiseBill.objects.all()
    serializer_class = PromiseBillSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PromiseBillFilter


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def promise_bill_detail(request, pk):
    try:
        promise_bill = PromiseBill.objects.get(pk=pk)
    except Promise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PromiseBillSerializer(promise_bill)
        return Response(serializer.data)


class SuggestedPromiseBillFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = SuggestedPromiseBill
        fields = ['bill', 'promise']


class SuggestedPromiseBillList(generics.ListAPIView):
    queryset = SuggestedPromiseBill.objects.all()
    serializer_class = SuggestedPromiseBillSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = SuggestedPromiseBillFilter


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def suggested_promise_bill_detail(request, pk):
    try:
        suggested_promise_bill = SuggestedPromiseBill.objects.get(pk=pk)
    except Promise.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SuggestedPromiseBillSerializer(suggested_promise_bill)
        return Response(serializer.data)