from rest_framework import serializers
from .models import District

class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('name', 'id', 'abbreviation', 'created', 'modified')