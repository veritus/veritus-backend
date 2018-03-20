from rest_framework import generics
from .models import District
from .serializers import DistrictSerializer


class DistrictList(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class DistrictDetails(generics.RetrieveAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
