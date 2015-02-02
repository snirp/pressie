from django.conf.urls import patterns, url
from onderhoud import views

urlpatterns = patterns('',
    url(r'^begroting/(?P<pk>\d+)/$', views.begroting, name='begroting'),
    url(r'^conditiemeting/(?P<pk>\d+)/$', views.conditiemeting, name='conditiemeting'),
    url(r'^conditiefoto/(?P<pk>\d+)/$', views.conditiefoto, name='conditiefoto'),
)

