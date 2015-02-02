from django.conf.urls import patterns, url
from onderhoudapi import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^$', views.api_root),
    url(r'^complex/$', views.ComplexListAPI.as_view(), name='complex-list'),
    url(r'^complex/(?P<pk>\d+)/$', views.ComplexDetailAPI.as_view(), name='complex-detail'),
    url(r'^complexgroep/$', views.ComplexgroepListAPI.as_view(), name='complexgroep-list'),
    url(r'^complexgroep/(?P<pk>\d+)/$', views.ComplexgroepDetailAPI.as_view(), name='complexgroep-detail'),
    url(r'^scenario/(?P<pk>\d+)/$', views.ScenarioDetailAPI.as_view(), name='scenario-detail'),
    url(r'^scenariogroep/$', views.ScenariogroepListAPI.as_view(), name='scenariogroep-list'),
    url(r'^scenariogroep/(?P<pk>\d+)/$', views.ScenariogroepDetailAPI.as_view(), name='scenariogroep-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)