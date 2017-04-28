from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Party
from .serializers import PartySerializerRead


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def party_list(request):

    if request.method == 'GET':
        parties = Party.objects.all()
        serializer = PartySerializerRead(parties, many=True)
        return Response(serializer.data)