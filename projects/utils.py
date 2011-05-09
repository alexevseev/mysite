# -*- coding: utf-8 -*-
from projects.models import Projects

def get_latest_project():   
    try:
        latest_project = Projects.objects.order_by('-created')[0]
    except IndexError:
        latest_project = None
    return latest_project
