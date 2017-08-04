from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ParliamentSession, Parliament, ParliamentMember
from .serializers import ParliamentSessionSerializerRead
from .serializers import ParliamentSessionSerializerWrite
from .serializers import ParliamentSerializer
from .serializers import ParliamentMemberSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def parliament_list(request):
    '''
    get:
        Get a list of all parliments.

    post:
        Creates a new parliament.
    '''
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
    '''
    get:
        Get parliment by ID.

    put:
        Add new parliment with a given ID.

    delete:
        Remove parliment with a given ID.

    '''

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



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def parliament_session_list(request):
    '''
    get:
        Get a list of all parliment sessions.

    post:
        Add new parliment session.

    '''

    if request.method == 'GET':
        parliament_sessions = ParliamentSession.objects.all()
        parliament_read_serializer = ParliamentSessionSerializerRead(parliament_sessions, many=True)
        return Response(parliament_read_serializer.data)

    elif request.method == 'POST':
        parliament_write_serializer = ParliamentSessionSerializerWrite(data=request.data)
        if parliament_write_serializer.is_valid():
            parliament_write_serializer.save()
            return Response(parliament_write_serializer.data, status=status.HTTP_201_CREATED)
        return Response(parliament_write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def parliament_session_detail(request, pk):
    '''
    get:
        Get parliment session by ID.

    put:
        Add new parliment session with a given ID.

    delete:
        Remove parliment session with a given ID.

    '''

    try:
        parliament_session = ParliamentSession.objects.get(pk=pk)
    except ParliamentSession.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ps_read_serializer = ParliamentSessionSerializerRead(parliament_session)
        return Response(ps_read_serializer.data)

    elif request.method == 'PUT':
        ps_write_serializer = ParliamentSessionSerializerWrite(
            parliament_session,
            data=request.data
        )
        if ps_write_serializer.is_valid():
            ps_write_serializer.save()
            return Response(ps_write_serializer.data)
        return Response(ps_write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def parliamentMember_list(request):
    ''' Get detailed list of parliament members '''
    if request.method == 'GET':
        parliamentMembers = ParliamentMember.objects.all()
        serializer = ParliamentMemberSerializer(parliamentMembers, many=True)
        return Response(serializer.data)
