import datetime

from django.db.models.query import Q
from django.http import HttpResponseRedirect

from overseer import context_processors
from overseer.models import Service, Event

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
    
    event_list = list(Event.objects\
                             .filter(Q(status__gt=0) | Q(date_updated__gte=datetime.datetime.now()-datetime.timedelta(days=1)))\
                             .order_by('-date_created')[0:5])
    
    if event_list:
        latest_event, event_list = event_list[0], event_list[1:]
    else:
        latest_event = None
    
    return respond('overseer/index.html', {
        'service_list': service_list,
        'event_list': event_list,
        'latest_event': latest_event,
    }, request)

def service(request, slug):
    "Displays a list of all services and their current status."
    
    service = Service.objects.get(slug=slug)
    
    event_list = service.event_set.order_by('-date_created')
    
    return respond('overseer/service.html', {
        'service': service,
        'event_list': event_list,
    }, request)

def event(request, id):
    "Displays a list of all services and their current status."
    
    event = Event.objects.get(pk=id)
    
    return respond('overseer/event.html', {
        'event': event,
    }, request)

def last_event(request, slug):
    "Displays a list of all services and their current status."
    
    service = Service.objects.get(slug=slug)
    
    try:
        event = service.event_set.order_by('-date_created')[0]
    except IndexError:
        return HttpResponseRedirect(service.get_absolute_url())
    
    return respond('overseer/event.html', {
        'event': event,
    }, request)