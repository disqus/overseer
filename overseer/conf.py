from django.conf import settings

base = getattr(settings, 'OVERSEER_CONFIG', {})

TITLE = base.get('TITLE', 'Service Status')
NAME = base.get('NAME', 'Service Status')
MEDIA_PREFIX = base.get('MEDIA_PREFIX', None)