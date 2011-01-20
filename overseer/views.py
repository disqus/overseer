from overseer import context_processors
from overseer.models import Service

def respond(template, context={}, request=None, **kwargs):
    "Calls render_to_response with a RequestConext"
    from django.http import HttpResponse
    from django.template import RequestContext
    from django.template.loader import render_to_string    

    if request:
        default = context_processors.default(request)
        default.update(context)
    else:
        default = context.copy()
    
    rendered = render_to_string(template, default, context_instance=request and RequestContext(request) or None)
    return HttpResponse(rendered, **kwargs)

def index(request):
    "Displays a list of all services and their current status."
    
    service_list = Service.objects.all()
    
    return respond('overseer/index.html', {
        'service_list': service_list,
    }, request)