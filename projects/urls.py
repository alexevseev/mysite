# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('projects.views',
    url(r'^all/$', 'show_projects', name='projects_url'),
    url(r'^(?P<slug>.+)/$', 'show_one_project', name='one_project_url'),
)