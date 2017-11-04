from rest_framework import serializers
from parliament.serializers import ParliamentMemberSerializer
from .models import Case, CaseCreator

class CaseCreatorSerializer(serializers.ModelSerializer):
    parliament_member = ParliamentMemberSerializer()
    class Meta:
        model = CaseCreator
        fields = (
            'parliament_member',
        )

class CaseSerializer(serializers.ModelSerializer):

    parliament_session = serializers.PrimaryKeyRelatedField(read_only=True)
    case_creators = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Case
        fields = (
            'id',
            'name',
            'number',
            'case_type',
            'althingi_status',
            'status',
            'parliament_session',
            'created',
            'modified',
            'althingi_link',
            'case_creators'
        )
