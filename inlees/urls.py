from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^scenario/(?P<pk>\d+)/$', 'inlees.views.singlezip_upload', name='singleimportform'),
    url(r'^scenario/$', 'inlees.views.zip_upload', name='importform'),
    )
