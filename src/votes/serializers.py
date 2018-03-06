from rest_framework import serializers
from .models import Vote, VoteRecord
from parliament.serializers import ParliamentMemberSerializer

class VoteSerializer(serializers.ModelSerializer):
    vote_record = serializers.PrimaryKeyRelatedField(read_only=True)
    parliament_member = ParliamentMemberSerializer(read_only=True)
    class Meta:
        model = Vote
        fields = (
            'parliament_member',
            'althingi_result',
            'vote_record',
        )

class VoteRecordSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)
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

