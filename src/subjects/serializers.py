from rest_framework import serializers
from case_gather.models import Subject
from .models import CaseSubject, PromiseSubject


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'created',
            'modified',
            'description',
            'parliament_session',
            'number',
            'parent'
        )


class CaseSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseSubject
        fields = ('id', 'subject', 'created', 'modified')


class PromiseSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromiseSubject
        fields = ('id', 'subject', 'promise', 'created', 'modified')
