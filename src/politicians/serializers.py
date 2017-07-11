from rest_framework import serializers
from party.serializers import PartySerializerRead
from district.serializers import DistrictSerializerRead
from promises.serializers import PromiseSerializerRead
from .models import Politician


class PoliticianSerializer(serializers.ModelSerializer):

    party = PartySerializerRead()
    district = DistrictSerializerRead()
    promises = PromiseSerializerRead(many=True, read_only=True)

    class Meta:
        model = Politician
        fields = ('name', 'id', 'initials', 'districtNumber', 'party', 'district', 'promises')
