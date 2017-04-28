from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import CaseSubject, PromiseSubject
from case_gather.models import Subject
from .serializers import SubjectSerializer, CaseSubjectSerializer, PromiseSubjectSerializerWrite, PromiseSubjectSerializerRead
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def subject_list(request):

    if request.method == 'GET':
        all_subjects = Subject.objects.all()
        serializer = SubjectSerializer(all_subjects, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def subject_promises_list(request):

    if request.method == 'GET':
        all_tags = PromiseSubject.objects.all()
        serializer = PromiseSubjectSerializerRead(all_tags, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PromiseSubjectSerializerWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
