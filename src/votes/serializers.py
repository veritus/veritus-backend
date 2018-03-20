from rest_framework import serializers
from .models import Vote, VoteRecord


class VoteRecordSerializer(serializers.ModelSerializer):
    votes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = VoteRecord
        fields = (
            'case',
            'althingi_id',
            'yes',
            'no',
            'didNotVote',
            'althingi_result',
            'votes',
        )


class VoteSerializer(serializers.ModelSerializer):
    vote_record = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = (
            'parliament_member',
            'althingi_result',
            'vote_record',
        )
