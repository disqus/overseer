"""
overseer.tests.urls
~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2011 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from django.conf.urls.defaults import *

from django.contrib import admin

admin.autodiscover()

def handler500(request):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError
    from overseer.context_processors import default
    import logging
    import sys
    try:
        context = default(request)
    except Exception, e:
        logging.error(e, exc_info=sys.exc_info(), extra={'request': request})
        context = {}
    
    context['request'] = request
    
    t = loader.get_template('500.html') # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context(context)))

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('overseer.urls', namespace='overseer')),
)