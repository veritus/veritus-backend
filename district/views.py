from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import District
from .serializers import DistrictSerializerRead

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def district_list(request):

    if request.method == 'GET':
        districts = District.objects.all()
        serializer = DistrictSerializerRead(districts, many=True)
        return Response(serializer.data)
