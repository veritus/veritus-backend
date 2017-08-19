from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from social_django.utils import psa
from rest_framework.decorators import api_view

@psa('social:complete')
@api_view(['GET'])
def login_with_access_token(request, backend):
    """
    Social media login
    """
    token = request.GET.get('access_token')
    user = request.backend.do_auth(token)
    if user:
        login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
