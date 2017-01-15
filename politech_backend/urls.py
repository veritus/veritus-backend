from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from promises import views as promise_views
from bill_gather import views as bill_views
from parliament import views as parliament_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^promises/$', promise_views.promise_list),
    url(r'^promises/(?P<pk>[0-9]+)$', promise_views.promise_detail),
    url(r'^promiseBills/$', promise_views.promise_bill_list),
    url(r'^promiseBills/(?P<pk>[0-9]+)$', promise_views.promise_bill_detail),
    url(r'^suggestedPromiseBills/$', promise_views.SuggestedPromiseBillList.as_view()),
   # url(r'^suggestedPromiseBills/(?P<pk>[0-9]+)$', promise_views.suggested_promise_bill_detail),
    url(r'^bills/$', bill_views.bill_list),
    url(r'^bills/(?P<pk>[0-9]+)$', bill_views.bill_detail),
    url(r'^parliaments/$', parliament_views.parliament_list),
    url(r'^parliaments/(?P<pk>[0-9]+)$', parliament_views.parliament_detail),
    url(r'^parliamentSessions/$', parliament_views.parliament_session_list),
    url(r'^parliamentSessions/(?P<pk>[0-9]+)$', parliament_views.parliament_session_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)