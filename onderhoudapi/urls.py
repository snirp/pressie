from django.conf.urls import patterns, url
from onderhoudapi import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^$', views.api_root),
    url(r'^complex/$', views.ComplexListAPI.as_view(), name='complex-list'),
    url(r'^complex/(?P<pk>\d+)/$', views.ComplexDetailAPI.as_view(), name='complex-detail'),
    url(r'^complexgroep/$', views.ComplexgroepListAPI.as_view(), name='complexgroep-list'),
    url(r'^complexgroep/(?P<pk>\d+)/$', views.ComplexgroepDetailAPI.as_view(), name='complexgroep-detail'),
    url(r'^scenario/$', views.ScenarioListAPI.as_view(), name='scenario-list'),
    url(r'^scenario/(?P<pk>\d+)/$', views.ScenarioDetailAPI.as_view(), name='scenario-detail'),
    url(r'^scenariogroep/$', views.ScenariogroepListAPI.as_view(), name='scenariogroep-list'),
    url(r'^scenariogroep/(?P<pk>\d+)/$', views.ScenariogroepDetailAPI.as_view(), name='scenariogroep-detail'),
    url(r'^conditiefoto/(?P<pk>\d+)/$', views.ConditiefotoDetail.as_view({
        'get': 'list',
        'post': 'create',
        'delete': 'destroy'}), name='conditiefoto-detail'),
    url(r'^gebrek/$', views.GebrekListAPI.as_view(), name='gebrek-list'),
    url(r'^gebrek/(?P<pk>\d+)/$', views.GebrekDetailAPI.as_view(), name='gebrek-detail'),
    url(r'^conditiedeel/$', views.ConditiedeelListAPI.as_view(), name='conditiedeel-list'),
    url(r'^conditiedeel/(?P<pk>\d+)/$', views.ConditiedeelDetailAPI.as_view(), name='conditiedeel-detail'),
    url(r'^conditiegroep/$', views.ConditiegroepListAPI.as_view(), name='conditiegroep-list'),
    url(r'^conditiegroep/(?P<pk>\d+)/$', views.ConditiegroepDetailAPI.as_view(), name='conditiegroep-detail'),
    url(r'^conditiemeting/$', views.ConditiemetingListAPI.as_view(), name='conditiemeting-list'),
    url(r'^conditiemeting/(?P<pk>\d+)/$', views.ConditiemetingDetailAPI.as_view(), name='conditiemeting-detail')
)

urlpatterns = format_suffix_patterns(urlpatterns)