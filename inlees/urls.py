from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^scenario/(?P<pk>\d+)/$', 'inlees.views.zip_upload', name='importform'),
    )
