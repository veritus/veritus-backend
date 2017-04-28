from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import CaseSubject, PromiseSubject
from case_gather.models import Subject
from .serializers import SubjectSerializer, CaseSubjectSerializer, PromiseSubjectSerializerWrite, PromiseSubjectSerializerRead
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import generics
import django_filters
        

class PromiseSubjectList(generics.ListAPIView):
    queryset = PromiseSubject.objects.all()
    serializer_class = PromiseSubjectSerializerRead
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('promise', 'subject')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def post(self, request):
        serializer = PromiseSubjectSerializerWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('name', 'parent', 'number', 'parliament_session')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)