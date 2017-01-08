from rest_framework import serializers, viewsets
from .models import Promise
from bill_gather.serializers import ParliamentSerializer


class PromiseSerializer(serializers.HyperlinkedModelSerializer):

    parliament = ParliamentSerializer()

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament')


class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer


