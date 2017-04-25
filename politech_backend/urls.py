from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from promises import views as promise_views
from case_gather import views as case_views
from parliament import views as parliament_views
from party import views as party_views
from district import views as district_views

urlpatterns = [
    url(r'^api/v1/admin/', admin.site.urls),
    url(r'^api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/promises/$', promise_views.promise_list),
    url(r'^api/v1/promises/(?P<pk>[0-9]+)$', promise_views.promise_detail),
    url(r'^api/v1/promiseCases/$', promise_views.PromiseCaseList.as_view()),
    url(r'^api/v1/promiseCases/(?P<pk>[0-9]+)$', promise_views.promise_case_detail),
    url(r'^api/v1/suggestedPromiseCases/$', promise_views.SuggestedPromiseCaseList.as_view()),
    url(r'^api/v1/suggestedPromiseCases/(?P<pk>[0-9]+)$', promise_views.suggested_promise_case_detail),
    url(r'^api/v1/cases/$', case_views.case_list),
    url(r'^api/v1/cases/(?P<pk>[0-9]+)$', case_views.case_detail),
    url(r'^api/v1/parliaments/$', parliament_views.parliament_list),
    url(r'^api/v1/parliaments/(?P<pk>[0-9]+)$', parliament_views.parliament_detail),
    url(r'^api/v1/parliamentSessions/$', parliament_views.parliament_session_list),
    url(r'^api/v1/parliamentSessions/(?P<pk>[0-9]+)$', parliament_views.parliament_session_detail),
    url(r'^api/v1/parties/$', party_views.party_list),
    url(r'^api/v1/parliamentMembers/$', parliament_views.parliamentMember_list),
    url(r'^api/v1/districts/$', district_views.district_list),
    url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
    url(r'^api/v1/rest-auth/registration/', include('rest_auth.registration.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
