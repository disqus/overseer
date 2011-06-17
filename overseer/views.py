"""
overseer.views
~~~~~~~~~~~~~~

:copyright: (c) 2011 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import datetime
import urlparse

from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models.query import Q
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from overseer import context_processors, conf
from overseer.forms import NewSubscriptionForm, UpdateSubscriptionForm
from overseer.models import Service, Event, Subscription, UnverifiedSubscription

def requires(value_or_callable):
    def wrapped(func):
        def call(request, *args, **kwargs):
            if callable(value_or_callable):
                result = value_or_callable(request)
            else:
                result = value_or_callable
            
            if not result:
                return HttpResponseRedirect(reverse('overseer:index'))
            
            return func(request, *args, **kwargs)
        return call
    return wrapped

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
                             .order_by('-date_created')[0:6])
    
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
    
    try:
        service = Service.objects.get(slug=slug)
    except Service.DoesNotExist:
        return HttpResponseRedirect(reverse('overseer:index'))
        
    event_list = service.event_set.order_by('-date_created')
    
    return respond('overseer/service.html', {
        'service': service,
        'event_list': event_list,
    }, request)

def event(request, id):
    "Displays a list of all services and their current status."
    
    try:
        evt = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return HttpResponseRedirect(reverse('overseer:index'))
    
    update_list = list(evt.eventupdate_set.order_by('-date_created'))
    
    return respond('overseer/event.html', {
        'event': evt,
        'update_list': update_list,
    }, request)

def last_event(request, slug):
    "Displays a list of all services and their current status."
    
    try:
        service = Service.objects.get(slug=slug)
    except Service.DoesNotExist:
        return HttpResponseRedirect(reverse('overseer:index'))
    
    try:
        evt = service.event_set.order_by('-date_created')[0]
    except IndexError:
        return HttpResponseRedirect(service.get_absolute_url())
    
    return event(request, evt.pk)

@requires(conf.ALLOW_SUBSCRIPTIONS)
@csrf_protect
def update_subscription(request, ident):
    "Shows subscriptions options for a verified subscriber."
    
    try:
        subscription = Subscription.objects.get(ident=ident)
    except Subscription.DoesNotExist:
        return respond('overseer/invalid_subscription_token.html', {}, request)

    if request.POST:
        form = UpdateSubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            if form.cleaned_data['unsubscribe']:
                subscription.delete()
        
                return respond('overseer/unsubscribe_confirmed.html', {
                    'email': subscription.email,
                })
            else:
                form.save()

            return HttpResponseRedirect(request.get_full_path())
    else:
        form = UpdateSubscriptionForm(instance=subscription)
        
    context = csrf(request)
    context.update({
        'form': form,
        'subscription': subscription,
        'service_list': Service.objects.all(),
    })

    return respond('overseer/update_subscription.html', context, request)

@requires(conf.ALLOW_SUBSCRIPTIONS)
@csrf_protect
def create_subscription(request):
    "Shows subscriptions options for a new subscriber."
    
    if request.POST:
        form = NewSubscriptionForm(request.POST)
        if form.is_valid():
            unverified = form.save()

            body = """Please confirm your email address to subscribe to status updates from %(name)s:\n\n%(link)s""" % dict(
                name=conf.NAME,
                link=urlparse.urljoin(conf.BASE_URL, reverse('overseer:verify_subscription', args=[unverified.ident]))
            )

            # Send verification email
            from_mail = conf.FROM_EMAIL
            if not from_mail:
                from_mail = 'overseer@%s' % request.get_host().split(':', 1)[0]
            
            send_mail('Confirm Subscription', body, from_mail, [unverified.email],
                      fail_silently=True)
            
            # Show success page
            return respond('overseer/create_subscription_complete.html', {
                'subscription': unverified,
            }, request)
    else:
        form = NewSubscriptionForm()

    context = csrf(request)
    context.update({
        'form': form,
        'service_list': Service.objects.all(),
    })

    return respond('overseer/create_subscription.html', context, request)

@requires(conf.ALLOW_SUBSCRIPTIONS)
def verify_subscription(request, ident):
    """
    Verifies an unverified subscription and create or appends
    to an existing subscription.
    """
    
    try:
        unverified = UnverifiedSubscription.objects.get(ident=ident)
    except UnverifiedSubscription.DoesNotExist:
        return respond('overseer/invalid_subscription_token.html', {}, request)
    
    subscription = Subscription.objects.get_or_create(email=unverified.email, defaults={
        'ident': unverified.ident,
    })[0]

    subscription.services = unverified.services.all()
    
    unverified.delete()
    
    return respond('overseer/subscription_confirmed.html', {
        'subscription': subscription,
    }, request)