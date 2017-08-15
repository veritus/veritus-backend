""" Webservice endpoints for bills """

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Case
from .serializers import CaseSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def case_list(request):
    '''
    get:
        Get a list of all cases.
    '''
    if request.method == 'GET':
        cases = Case.objects.all()
        serializer = CaseSerializer(cases, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def case_detail(request, pk):
    '''
    get:
        Get case by ID.
    '''
    try:
        case = Case.objects.get(pk=pk)
    except Case.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CaseSerializer(case)
        return Response(serializer.data)
