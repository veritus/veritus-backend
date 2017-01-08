from rest_framework import serializers
from .models import ParliamentSession, Parliament


class ParliamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parliament
        fields = ('name','id')


class ParliamentSessionSerializerRead(serializers.ModelSerializer):

    parliament = ParliamentSerializer()

    class Meta:
        model = ParliamentSession
        fields = ('session_number', 'parliament', 'name', 'created', 'modified')


class ParliamentSessionSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = ParliamentSession
        fields = ('session_number', 'parliament', 'name', 'created', 'modified')







