from rest_framework import serializers, viewsets
from .models import Promise
from bill_gather.serializers import ParliamentSerializer


class PromiseSerializer_read(serializers.ModelSerializer):

    parliament = ParliamentSerializer(read_only=True)

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament', 'id', 'created', 'modified')


class PromiseSerializer_write(serializers.ModelSerializer):

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament', 'id', 'created', 'modified')




