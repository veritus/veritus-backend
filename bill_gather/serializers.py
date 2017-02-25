""" Bill serializer """
from rest_framework import serializers
from parliament.serializers import ParliamentSessionSerializerRead
from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    """ Bill serializer """
    parliament_session = ParliamentSessionSerializerRead()

    class Meta:
        model = Bill
        fields = ('name', 'description_link', 'althingi_created', 'number', 'id', 'parliament_session', 'created', 'modified')






