from rest_framework import serializers
from .models import ParliamentSession, Parliament, ParliamentMember
from party.serializers import PartySerializerRead
from district.serializers import DistrictSerializer

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

class ParliamentMemberSerializer(serializers.ModelSerializer):

    party = PartySerializerRead()
    district = DistrictSerializer()

    class Meta:
        model = ParliamentMember
        fields = ('name', 'id', 'initials', 'districtNumber', 'party', 'district')





