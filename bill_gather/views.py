""" Webservice endpoints for bills """

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .models import Bill
from .serializers import BillSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def bill_list(request):
    """ GET All and POST endpoint """
    if request.method == 'GET':
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def bill_detail(request, bill_id):
    """ GET by Id, PUT and DELETE endpoint """
    try:
        bill = Bill.objects.get(pk=bill_id)
    except Bill.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BillSerializer(bill)
        return Response(serializer.data)
