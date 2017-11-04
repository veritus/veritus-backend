from rest_framework import serializers
from promises.serializers import PromiseSerializerRead
from .models import Politician

class PoliticianSerializer(serializers.ModelSerializer):

    party = serializers.PrimaryKeyRelatedField(read_only=True)
    district = serializers.PrimaryKeyRelatedField(read_only=True)
    promises = PromiseSerializerRead(many=True, read_only=True)

    class Meta:
        model = Politician
        fields = ('name', 'id', 'initials', 'districtNumber', 'party', 'district', 'promises')
