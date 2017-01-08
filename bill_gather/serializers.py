from rest_framework import serializers, viewsets
from .models import Bill


class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        fields = ('name', 'description_link', 'created_date', 'number')

# ViewSets define the view behavior.
class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer