from rest_framework import serializers

from parliament.serializers import ParliamentSerializer
from case_gather.serializers import CaseSerializer

from .models import Promise, PromiseCase


class PromiseSerializerRead(serializers.ModelSerializer):
    ''' Serializer when reading promises (GET) '''

    parliament = ParliamentSerializer(read_only=True)

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


class PromiseSerializerWrite(serializers.ModelSerializer):
    ''' Serializer when writing to promises (POST, PUT) '''

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

    case = CaseSerializer(read_only=True)
    promise = PromiseSerializerRead(read_only=True)

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

