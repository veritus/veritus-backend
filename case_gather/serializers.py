from rest_framework import serializers
from .models import Bill
from parliament.serializers import ParliamentSessionSerializerRead


class BillSerializer(serializers.ModelSerializer):

    parliament_session = ParliamentSessionSerializerRead()

    class Meta:
        model = Bill
        fields = ('name', 'description_link', 'althingi_created', 'number', 'id', 'parliament_session', 'created', 'modified')






