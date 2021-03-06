from rest_framework import status, generics, viewsets
from rest_framework.response import Response
import django_filters

from case_gather.models import Subject
from .serializers import SubjectSerializer
from .serializers import PromiseSubjectSerializer
from .models import PromiseSubject


class PromiseSubjectList(viewsets.ModelViewSet):
    queryset = PromiseSubject.objects.all()
    serializer_class = PromiseSubjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('promise', 'subject')


class SubjectFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Subject
        fields = {
            'name': ['startswith', 'exact', 'contains', 'istartswith'],
            'parent': ['exact'],
            'number': ['exact'],
            'parliament_session': ['exact']
        }


class SubjectList(generics.ListAPIView):
    '''
    get:
        Get all subjects.

    post:
        Add new subjects.
    '''
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = SubjectFilter

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            # We capitalize the subject as we only want to have capitalized subjects
            serializer.validated_data['name'] = serializer.validated_data['name'].capitalize(
            )

            validated_subject = serializer.validated_data
            subject_exists = Subject.objects.filter(
                name=validated_subject['name'])

            if subject_exists.exists():
                # If the subject already exists, we dont want to create a duplicate.
                # Then we simply return the already existing object with a 200.
                exists_serializer = SubjectSerializer(subject_exists.get())
                return Response(exists_serializer.data, status=status.HTTP_200_OK)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
