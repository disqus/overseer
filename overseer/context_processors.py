from django.core.urlresolvers import reverse

import overseer
from overseer import conf

def default(request):
    return {
        'request': request,
        'OVERSEER_TITLE': conf.TITLE,
        'OVERSEER_NAME': conf.NAME,
        'OVERSEER_MEDIA_PREFIX': (conf.MEDIA_PREFIX or reverse('overseer:media')).rstrip('/'),
        'OVERSEER_VERSION': overseer.VERSION,
        'OVERSEER_ALLOW_SUBSCRIPTIONS': conf.ALLOW_SUBSCRIPTIONS,
    }