from rest_framework import serializers

from politicians.models import Politician
from promises.models import Promise

from .models import District

class PromiseField(serializers.ModelSerializer):
    class Meta:
        model = Promise
        fields = (
            'name',
            'id',
            'fulfilled'
        )

class PoliticianSerializer(serializers.ModelSerializer):

    party = serializers.PrimaryKeyRelatedField(read_only=True)
    promises = PromiseField(many=True, read_only=True)

    class Meta:
        model = Politician
        fields = (
            'name',
            'id',
            'initials',
            'party',
            'promises'
            )



class DistrictSerializer(serializers.ModelSerializer):
    politicians = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = District
        fields = (
            'name',
            'id',
            'abbreviation',
            'politicians',
            'created',
            'modified'
            )
