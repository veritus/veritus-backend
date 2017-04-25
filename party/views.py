from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .models import Party
from .serializers import PartySerializerRead, PartySerializerWrite

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def party_list(request):

    if request.method == 'GET':
        parties = Party.objects.all()
        serializer = PartySerializerRead(parties, many=True)
        return Response(serializer.data)