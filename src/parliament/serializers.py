from rest_framework import serializers
from .models import ParliamentSession, Parliament, ParliamentMember


class ParliamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parliament
        fields = (
            'name',
            'id'
        )


class ParliamentSessionSerializer(serializers.ModelSerializer):

    parliament = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ParliamentSession
        fields = ('session_number', 'parliament',
                  'name', 'created', 'modified')


class ParliamentMemberSerializer(serializers.ModelSerializer):

    party = serializers.PrimaryKeyRelatedField(read_only=True)
    district = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ParliamentMember
        fields = ('name', 'id', 'initials',
                  'districtNumber', 'party', 'district')
