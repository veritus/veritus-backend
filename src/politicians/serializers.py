from rest_framework import serializers
from .models import Politician


class PoliticianSerializer(serializers.ModelSerializer):

    party = serializers.PrimaryKeyRelatedField(read_only=True)
    district = serializers.PrimaryKeyRelatedField(read_only=True)
    promises = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Politician
        fields = ('name', 'id', 'initials', 'districtNumber',
                  'party', 'district', 'promises')
