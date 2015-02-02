from django.conf.urls import patterns, url
from organisatie import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^gebruikers$', views.GebruikerList.as_view(), name='gebruiker_list'),
    url(r'^gebruikers/(?P<pk>\d+)/$', views.GebruikerDetail.as_view(), name='gebruiker_detail'),
    )

urlpatterns = format_suffix_patterns(urlpatterns)
