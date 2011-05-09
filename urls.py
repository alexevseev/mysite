# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', include('home.urls')),
    (r'^projects/', include('projects.urls')),    
    (r'^services/', include('services.urls')),    
    (r'^accounts/', include('authorization.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^search/', include('haystack.urls')),
    (r'^about/', include('about.urls')),
    (r'^ajax/', include('ajax.urls')),
)

from django.conf import settings
if settings.LOCAL:
    print "LOCAL!"
    urlpatterns += patterns('',
        # This is for the CSS and static files:
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )