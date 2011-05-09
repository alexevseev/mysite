# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from projects.utils import get_latest_project
from services.utils import get_latest_service
   
    
def show_home(request):
    latest_project = get_latest_project()
    latest_service = get_latest_service()
    template_context = {'project':latest_project,
                        'service':latest_service,
                        'max_description_words': settings.BRIEF_WORDS_AMT}
    return render_to_response('home.html', template_context, RequestContext(request)) 
    