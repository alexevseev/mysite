# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('services.views',
    url(r'^all/$', 'show_services', name='services_url'),
    url(r'^(?P<slug>.+)/$', 'show_service', name='service_url'),
)