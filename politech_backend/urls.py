from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from promises import views as promise_views
from bill_gather import views as bill_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^promises/$', promise_views.promise_list),
    url(r'^promises/(?P<pk>[0-9]+)$', promise_views.promise_detail),
    url(r'^bills/$', bill_views.bill_list),
    url(r'^bills/(?P<pk>[0-9]+)$', bill_views.bill_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)