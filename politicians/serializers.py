from rest_framework import serializers
from .models import Politician
from parliament.serializers import PartySerializerRead
from district.serializers import DistrictSerializer


class PoliticianSerializer(serializers.ModelSerializer):

    party = PartySerializerRead()
    district = DistrictSerializer()

    class Meta:
        model = Politician
        fields = ('name', 'id', 'initials', 'districtNumber', 'party', 'district')





