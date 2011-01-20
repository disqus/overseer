from django.core.urlresolvers import reverse

from overseer import conf

def default(request):
    return {
        'request': request,
        'OVERSEER_TITLE': conf.TITLE,
        'OVERSEER_NAME': conf.NAME,
        'OVERSEER_MEDIA_PREFIX': conf.MEDIA_PREFIX or reverse('overseer:media'),
    }