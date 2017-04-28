from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Tag, CaseTags, PromiseTags
from .serializers import PromiseSerializerRead, PromiseSerializerWrite, PromiseCaseSerializer, SuggestedPromiseCaseSerializer
from rest_framework.permissions import IsAuthenticated,

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def tag_list(request):
    serializer = PromiseSerializerWrite(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
