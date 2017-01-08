from rest_framework import serializers, viewsets
from .models import Promise
from bill_gather.serializers import ParliamentSerializer


class PromiseSerializer(serializers.HyperlinkedModelSerializer):

    parliament_session = ParliamentSerializer()

    class Meta:
        model = Promise
        fields = ('name', 'small_description', 'long_description', 'parliament_session')


class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer


