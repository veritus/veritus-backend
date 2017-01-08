from rest_framework import serializers, viewsets
from .models import Bill, ParliamentSession, Parliament


class ParliamentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Parliament
        fields = ('name','id')


class ParliamentViewSet(viewsets.ModelViewSet):
    queryset = Parliament.objects.all()
    serializer_class = ParliamentSerializer


class ParliamentSessionSerializer(serializers.HyperlinkedModelSerializer):

    parliament = ParliamentSerializer()

    class Meta:
        model = ParliamentSession
        fields = ('session_number', 'parliament')


class ParliamentSessionViewSet(viewsets.ModelViewSet):
    queryset = ParliamentSession.objects.all()
    serializer_class = ParliamentSessionSerializer


class BillSerializer(serializers.HyperlinkedModelSerializer):

    session = ParliamentSessionSerializer()

    class Meta:
        model = Bill
        fields = ('name', 'description_link', 'created_date', 'number', 'id', 'session')


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


