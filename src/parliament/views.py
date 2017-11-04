import django_filters

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ParliamentSession, Parliament, ParliamentMember
from .serializers import ParliamentSessionSerializer
from .serializers import ParliamentSerializer
from .serializers import ParliamentMemberSerializer

class ParliamentList(generics.ListAPIView):
    queryset = Parliament.objects.all()
    serializer_class = ParliamentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class ParliamentDetails(generics.RetrieveAPIView):
    queryset = Parliament.objects.all()
    serializer_class = ParliamentSerializer

class ParliamentSessionList(generics.ListAPIView):
    queryset = ParliamentSession.objects.all()
    serializer_class = ParliamentSessionSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('parliament',)
    permission_classes = (IsAuthenticatedOrReadOnly,)

class ParliamentSessionDetails(generics.RetrieveAPIView):
    queryset = ParliamentSession.objects.all()
    serializer_class = ParliamentSessionSerializer

class ParliamentMemberList(generics.ListAPIView):
    queryset = ParliamentMember.objects.all()
    serializer_class = ParliamentMemberSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('party', 'district')
    permission_classes = (IsAuthenticatedOrReadOnly,)
