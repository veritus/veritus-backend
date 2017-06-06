from rest_framework import serializers
from .models import Politician
from party.serializers import PartySerializerRead
from district.serializers import DistrictSerializer
from promises.serializers import PromiseSerializerRead


class PoliticianSerializer(serializers.ModelSerializer):

    party = PartySerializerRead()
    district = DistrictSerializer()
    promises = PromiseSerializerRead(many=True, read_only=True)

    class Meta:
        model = Politician
        fields = ('name', 'id', 'initials', 'districtNumber', 'party', 'district', 'promises')





