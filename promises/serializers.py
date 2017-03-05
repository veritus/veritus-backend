from rest_framework import serializers, viewsets
from .models import Promise
from parliament.serializers import ParliamentSerializer
from case_gather.serializers import CaseSerializer

class PromiseSerializerRead(serializers.ModelSerializer):

    parliament = ParliamentSerializer(read_only=True)

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament', 'id', 'created', 'modified')


class PromiseSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament', 'id', 'created', 'modified')


class PromiseCaseSerializer(serializers.ModelSerializer):

    case = CaseSerializer(read_only=True)
    promise = PromiseSerializerRead(read_only=True)

    class Meta:
        model = Promise
        fields = ('name', 'case', 'promise', 'id', 'created', 'modified')


class SuggestedPromiseCaseSerializer(serializers.ModelSerializer):

    case = CaseSerializer(read_only=True)
    promise = PromiseSerializerRead(read_only=True)

    class Meta:
        model = Promise
        fields = ('name', 'case', 'promise', 'id', 'created', 'modified')
