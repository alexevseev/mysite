from services.models import Services
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def show_services(request):    
    template_context = {'services': Services.objects.all(),}
    return render_to_response('services/all.html', template_context, RequestContext(request))  
    
    
def show_service(request, slug):    
    current_service = get_object_or_404(Services, slug=slug)
    template_context = {'service':current_service,}
    return render_to_response('services/one.html', template_context, RequestContext(request)) 