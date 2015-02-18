from django.conf.urls import patterns, include, url
from django.contrib import admin
from pressie import settings

urlpatterns = patterns('',
    url(r'^$', 'onderhoud.views.home_page', name='home'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='mylogin'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='mylogout'),
    url(r'^onderhoud/', include('onderhoud.urls')),
    url(r'^onderhoudapi/', include('onderhoudapi.urls')),
    url(r'^inlees/', include('inlees.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )