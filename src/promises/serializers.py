from rest_framework import serializers

from parliament.serializers import ParliamentSerializer
from case_gather.serializers import CaseSerializer

from .models import Promise, PromiseCase

class PromiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promise
        fields = (
            'name',
            'small_description',
            'long_description',
            'parliament',
            'id',
            'created',
            'modified',
            'politician',
            'party',
            'fulfilled'
            )


class PromiseCaseSerializer(serializers.ModelSerializer):
    ''' Serializer for promise case connections '''

    case = serializers.PrimaryKeyRelatedField(read_only=True)
    promise = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PromiseCase
        fields = (
            'name',
            'case',
            'promise',
            'id',
            'created',
            'modified',
            'relationship_type',
            'percent_of_common_subjects',
        )
