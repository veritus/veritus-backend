from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Politician
from .serializers import PoliticianSerializer

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def politician_list(request):

    if request.method == 'GET':
        politicians = Politician.objects.all()
        serializer = PoliticianSerializer(politicians, many=True)
        return Response(serializer.data)
