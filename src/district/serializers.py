from rest_framework import serializers

from party.serializers import PartySerializerRead
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

    party = PartySerializerRead()
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



class DistrictSerializerRead(serializers.ModelSerializer):
    ''' Serializer when reading districts (GET) '''
    politicians = PoliticianSerializer(many=True, read_only=True)

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


class DistrictSerializerWrite(serializers.ModelSerializer):
    ''' Serializer when writing to districts (POST, PUT) '''

    class Meta:
        model = District
        fields = (
            'name',
            'id',
            'abbreviation',
            'created',
            'modified'
            )
