from rest_framework import serializers
from parliament.serializers import ParliamentSessionSerializerRead
from .models import Case

class CaseSerializer(serializers.ModelSerializer):

    parliament_session = ParliamentSessionSerializerRead()

    class Meta:
        model = Case
        fields = (
            'id',
            'name',
            'number',
            'case_type',
            'case_status',
            'parliament_session',
            'created',
            'modified',
            'althingi_link'
        )
