from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Promise
from .serializers import PromiseSerializerRead, PromiseSerializerWrite
from rest_framework import permissions


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