from rest_framework import serializers, viewsets
from .models import Promise
from parliament.serializers import ParliamentSerializer


class PromiseSerializerRead(serializers.ModelSerializer):

    parliament = ParliamentSerializer(read_only=True)

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament', 'id', 'created', 'modified')


class PromiseSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament', 'id', 'created', 'modified')




