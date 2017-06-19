from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import django_filters

from case_gather.models import Subject
from .serializers import SubjectSerializer
from .serializers import PromiseSubjectSerializerWrite
from .serializers import PromiseSubjectSerializerRead
from .models import PromiseSubject

class PromiseSubjectList(generics.ListAPIView):
    queryset = PromiseSubject.objects.all()
    serializer_class = PromiseSubjectSerializerRead
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('promise', 'subject')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        ps_write_serializer = PromiseSubjectSerializerWrite(data=request.data)
        if ps_write_serializer.is_valid():
            ps_write_serializer.save()
            return Response(ps_write_serializer.data, status=status.HTTP_201_CREATED)
        return Response(ps_write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Subject
        fields = {
            'name': ['startswith', 'exact', 'contains'],
            'parent': ['exact'],
            'number': ['exact'],
            'parliament_session': ['exact']
            }

class SubjectList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = SubjectFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
