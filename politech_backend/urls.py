from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from bill_gather.serializers import BillViewSet, ParliamentSessionViewSet, ParliamentViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'bills', BillViewSet)
router.register(r'parliament_session', ParliamentSessionViewSet)
router.register(r'parliament', ParliamentViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]