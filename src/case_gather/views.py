""" Webservice endpoints for cases """
import django_filters
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
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
