from rest_framework import serializers, viewsets
from .models import Promise
from parliament.serializers import ParliamentSerializer
from bill_gather.serializers import BillSerializer

class PromiseSerializerRead(serializers.ModelSerializer):

    parliament = ParliamentSerializer(read_only=True)

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament', 'id', 'created', 'modified')


class PromiseSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament', 'id', 'created', 'modified')


class PromiseBillSerializer(serializers.ModelSerializer):

    bill = BillSerializer(read_only=True)
    promise = PromiseSerializerRead(read_only=True)

    class Meta:
        model = Promise
        fields = ('name', 'bill', 'promise', 'id', 'created', 'modified')


class SuggestedPromiseBillSerializer(serializers.ModelSerializer):

    bill = BillSerializer(read_only=True)
    promise = PromiseSerializerRead(read_only=True)

    class Meta:
        model = Promise
        fields = ('name', 'bill', 'promise', 'id', 'created', 'modified')
