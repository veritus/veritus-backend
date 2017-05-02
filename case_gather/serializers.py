from rest_framework import serializers
from .models import Case
from parliament.serializers import ParliamentSessionSerializerRead


class CaseSerializer(serializers.ModelSerializer):

    parliament_session = ParliamentSessionSerializerRead()

    class Meta:
        model = Case
        fields = ('name', 'number', 'case_type', 'case_status',
                  'id', 'parliament_session', 'created', 'modified')

class SuperSubjectSerializer(serializers.ModelSerializer):

    parliament_session = ParliamentSessionSerializerRead()

    class Meta:
        model = SuperSubject
        fields = ('name', 'supersubject_id', 'id', 
            'parliament_session', 'created', 'modified')

class SubjectSerializer(serializers.ModelSerializer):

    parliament_session = ParliamentSessionSerializerRead()

    class Meta:
        model = Subject
        fields = ('name', 'subject_id', 'description', 'supersubject',
                  'id', 'parliament_session', 'created', 'modified')