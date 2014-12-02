from django.conf.urls import patterns, include, url
from django.contrib import admin
from pressie import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pressie.views.home', name='home'),
    url(r'^stam/', include('stam.urls')),
    url(r'^gebouw/', include('gebouw.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )