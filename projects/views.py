from projects.models import Projects, ProjectTags
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings

def show_projects(request):
    filteredProjects = Projects.objects.all()
    max_tags_amount = ProjectTags.objects.count()
    ckecked_tags = dict()    
    for count, tagFromGET in enumerate(request.GET):        
        if count > max_tags_amount:
            break     
        ckecked_tags[tagFromGET] = True
        filteredProjects = filteredProjects.filter(tags__name=tagFromGET)
    template_context = {'projects': filteredProjects, 
                        'tags': ProjectTags.objects.all(), 
                        'checked': ckecked_tags, 
                        'max_description_words': settings.BRIEF_WORDS_AMT}
    return render_to_response('projects/all.html', template_context, RequestContext(request))  
    
    
def show_one_project(request, slug):    
    current_project = get_object_or_404(Projects, slug=slug)
    template_context = {'project':current_project,
                        'signup_prefix': settings.PREFIX_SIGNUP,
                        'login_prefix': settings.PREFIX_LOGIN}
    return render_to_response('projects/one.html', template_context, RequestContext(request)) 