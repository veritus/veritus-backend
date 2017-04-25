from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .models import District
from .serializers import DistrictSerializer

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def district_list(request):

    if request.method == 'GET':
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)
