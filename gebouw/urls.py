from django.conf.urls import patterns, url


from gebouw import views

urlpatterns = patterns('',
    url(r'^$', views.ComplexIndex.as_view(), name='complex_list'),
    url(r'^(?P<pk>\d+)/$', views.ComplexDetail.as_view(), name='complex_detail'),
    url(r'^conditiemeting/(?P<pk>\d+)/$', views.ConditiemetingDetail.as_view(), name='conditiemeting_detail'),
    url(r'^cmgroepen/(?P<pk>\d+)/$', views.ConditiemetingGroepen.as_view(), name='conditiemeting_groepen'),
    url(r'^scenario/(?P<s_id>\d+)/$', views.scenario_detail, name='scenario_detail'),
    url(r'^scenario/(?P<s_id>\d+)/vverapport/$', views.scenario_report_vve, name='scenario_report_vve'),
    )
