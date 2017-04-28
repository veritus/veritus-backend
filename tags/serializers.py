from rest_framework import serializers, viewsets
from .models import Tag, CaseTags, PromiseTags

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', 'id', 'created', 'modified')


class CaseTagSerializer(serializers.ModelSerializer):

    tag = TagSerializer()

    class Meta:
        model = CaseTags
        fields = ('tag', 'id', 'created', 'modified')


class PromiseTagSerializer(serializers.ModelSerializer):

    tag = TagSerializer()

    class Meta:
        model = PromiseTags
        fields = ('tag', 'id', 'created', 'modified')