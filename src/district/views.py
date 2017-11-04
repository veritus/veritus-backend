from rest_framework import generics
from .models import District
from .serializers import DistrictSerializerRead

class DistrictList(generics.ListAPIView):
    ''' PromiseCaseList endpoint '''
    queryset = District.objects.all()
    serializer_class = DistrictSerializerRead
