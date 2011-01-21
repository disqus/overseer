from django.conf.urls.defaults import *

import os.path

urlpatterns = patterns('',
    url(r'^media/(?P<path>.+)?$', 'django.views.static.serve', {
        'document_root': os.path.join(os.path.dirname(__file__), 'media'),
        'show_indexes': True
    }, name='media'),

    url(r'^$', 'overseer.views.index', name='index'),
    url(r'^service/(?P<slug>[^/]+)/$', 'overseer.views.service', name='service'),
    url(r'^service/(?P<slug>[^/]+)/last-event/$', 'overseer.views.last_event', name='last_event'),
    url(r'^event/(?P<id>[^/]+)/$', 'overseer.views.event', name='event'),
    url(r'^(?P<id>\d+)$', 'django.views.generic.simple.redirect_to', {'url': 'event/%(id)d/'}, name='event_short'),
)