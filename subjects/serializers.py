from rest_framework import serializers, viewsets
from .models import CaseSubject, PromiseSubject
from promises.serializers import PromiseSerializerRead
from case_gather.models import Subject

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('id', 'name', 'created', 'modified', 'description', 'parliament_session', 'number', 'parent')


class CaseSubjectSerializer(serializers.ModelSerializer):

    subject = SubjectSerializer()

    class Meta:
        model = CaseSubject
        fields = ('id', 'subject', 'created', 'modified')


class PromiseSubjectSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = PromiseSubject
        fields = ('id', 'subject', 'promise', 'created', 'modified')


class PromiseSubjectSerializerRead(serializers.ModelSerializer):

    subject = SubjectSerializer()
    promise = PromiseSerializerRead()
    
    class Meta:
        model = PromiseSubject
        fields = ('id', 'subject', 'promise', 'created', 'modified')