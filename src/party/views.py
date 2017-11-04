from rest_framework import generics
from .models import Party
from .serializers import PartySerializer

class PartyList(generics.ListAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

class PartyDetails(generics.RetrieveAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
