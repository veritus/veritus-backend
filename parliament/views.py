from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import ParliamentSession, Parliament, ParliamentMember
from .serializers import ParliamentSessionSerializerRead, ParliamentSessionSerializerWrite, ParliamentSerializer, ParliamentMemberSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def parliament_list(request):

    if request.method == 'GET':
        parliaments = Parliament.objects.all()
        serializer = ParliamentSerializer(parliaments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ParliamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def parliament_detail(request, pk):
    try:
        parliament = Parliament.objects.get(pk=pk)
    except Parliament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ParliamentSerializer(parliament)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParliamentSerializer(parliament, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        parliament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def parliament_session_list(request):

    if request.method == 'GET':
        parliament_sessions = ParliamentSession.objects.all()
        serializer = ParliamentSessionSerializerRead(parliament_sessions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ParliamentSessionSerializerWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def parliament_session_detail(request, pk):
    try:
        parliament_session = ParliamentSession.objects.get(pk=pk)
    except ParliamentSession.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ParliamentSessionSerializerRead(parliament_session)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParliamentSessionSerializerWrite(parliament_session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        parliament_session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def parliamentMember_list(request):

    if request.method == 'GET':
        parliamentMembers = ParliamentMember.objects.all()
        serializer = ParliamentMemberSerializer(parliamentMembers, many=True)
        return Response(serializer.data)

