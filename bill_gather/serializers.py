from rest_framework import serializers, viewsets
from .models import Bill, ParliamentSession, Parliament


class ParliamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parliament
        fields = ('name','id')


class ParliamentSessionSerializer(serializers.ModelSerializer):

    parliament = ParliamentSerializer()

    class Meta:
        model = ParliamentSession
        fields = ('session_number', 'parliament', 'name', 'created', 'modified')


class BillSerializer(serializers.ModelSerializer):

    parliament_session = ParliamentSessionSerializer()

    class Meta:
        model = Bill
        fields = ('name', 'description_link', 'althingi_created', 'number', 'id', 'parliament_session', 'created', 'modified')






