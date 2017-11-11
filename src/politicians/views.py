from rest_framework import generics
from .models import Politician
from .serializers import PoliticianSerializer

class PoliticianList(generics.ListAPIView):
    queryset = Politician.objects.all()
    serializer_class = PoliticianSerializer

class PoliticianDetails(generics.RetrieveAPIView):
    queryset = Politician.objects.all()
    serializer_class = PoliticianSerializer
