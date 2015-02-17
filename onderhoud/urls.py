from django.conf.urls import patterns, url
from onderhoud import views

urlpatterns = patterns('',
    url(r'^complex/$', views.complex_list, name='complex_list'),
    url(r'^begroting/$', views.begroting_list, name='begroting-list'),
    url(r'^begroting/(?P<pk>\d+)/$', views.begroting, name='begroting'),
    url(r'^conditiemeting/$', views.conditiemetingen, name='conditiemeting_list'),
    url(r'^conditiemeting/(?P<pk>\d+)/$', views.conditiemeting, name='conditiemeting_detail'),
    url(r'^conditiefoto/(?P<pk>\d+)/$', views.conditiefoto, name='conditiefoto'),
    url(r'^gebreken/$', views.gebreken_tabel, name='gebreken_tabel')
)

