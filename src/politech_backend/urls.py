from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from promises import views as promise_views
from case_gather import views as case_views
from parliament import views as parliament_views
from party import views as party_views
from district import views as district_views
from subjects import views as subject_views
from politicians import views as politician_views
from votes import views as vote_views

schema_view = get_schema_view(
    title='Veritus API',
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer]
)

urlpatterns = [
    url(r'^$', schema_view, name="docs"),
    url(r'^api/v1/admin/', admin.site.urls),
    url(r'^api/v1/api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/promises/$', promise_views.PromiseList.as_view()),
    url(r'^api/v1/promises/(?P<pk>[0-9]+)$',
        promise_views.PromiseDetails.as_view()),
    url(r'^api/v1/promises/subjects/$',
        subject_views.PromiseSubjectList.as_view({'get': 'list', 'post': 'create'})),
    url(r'^api/v1/promises/subjects/(?P<pk>[0-9]+)$',
        subject_views.PromiseSubjectList.as_view({'get': 'detail', 'delete': 'destroy'})),
    url(r'^api/v1/promiseCases/$', promise_views.PromiseCaseList.as_view()),
    url(r'^api/v1/promiseCases/(?P<pk>[0-9]+)$',
        promise_views.PromiseCaseDetails.as_view()),
    url(r'^api/v1/cases/$', case_views.CaseList.as_view()),
    url(r'^api/v1/cases/(?P<pk>[0-9]+)$', case_views.CaseDetails.as_view()),
    url(r'^api/v1/parliaments/$', parliament_views.ParliamentList.as_view()),
    url(r'^api/v1/parliaments/(?P<pk>[0-9]+)$',
        parliament_views.ParliamentDetails.as_view()),
    url(r'^api/v1/parliamentSessions/$',
        parliament_views.ParliamentSessionList.as_view()),
    url(
        r'^api/v1/parliamentSessions/(?P<pk>[0-9]+)$',
        parliament_views.ParliamentSessionDetails.as_view()
    ),
    url(r'^api/v1/parties/$', party_views.PartyList.as_view()),
    url(r'^api/v1/parties/(?P<pk>[0-9]+)$',
        party_views.PartyDetails.as_view()),
    url(r'^api/v1/parliamentMembers/$',
        parliament_views.ParliamentMemberList.as_view()),
    url(
        r'^api/v1/parliamentMembers/(?P<pk>[0-9]+)$',
        parliament_views.ParliamentMemberDetails.as_view()
    ),
    url(r'^api/v1/politicians/$', politician_views.PoliticianList.as_view()),
    url(r'^api/v1/politicians/(?P<pk>[0-9]+)$',
        politician_views.PoliticianDetails.as_view()),
    url(r'^api/v1/districts/$', district_views.DistrictList.as_view()),
    url(r'^api/v1/districts/(?P<pk>[0-9]+)$',
        district_views.DistrictDetails.as_view()),
    url(r'^api/v1/subjects/$', subject_views.SubjectList.as_view()),
    url(r'^api/v1/voteRecord/$', vote_views.VoteRecordList.as_view()),
    url(r'^api/v1/vote/$', vote_views.VoteList.as_view()),

    url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
    url(r'^api/v1/rest-auth/registration/',
        include('rest_auth.registration.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += staticfiles_urlpatterns()
