from rest_framework import serializers
from .models import Party

class PartySerializerRead(serializers.ModelSerializer):

    class Meta:
        model = Party
        fields = ('name', 'id', 'website', 'created', 'modified')

class PartySerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = Party
        fields = ('name', 'website')
