"""
overseer.conf
~~~~~~~~~~~~~

:copyright: (c) 2011 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from django.conf import settings

base = getattr(settings, 'OVERSEER_CONFIG', {})

TITLE = base.get('TITLE', 'Service Status')
NAME = base.get('NAME', 'Service Status')
MEDIA_PREFIX = base.get('MEDIA_PREFIX', None)

TWITTER_CONSUMER_KEY = base.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = base.get('TWITTER_CONSUMER_SECRET')

# Run manage.py overseer_twitter_auth to generate an access key
TWITTER_ACCESS_TOKEN = base.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = base.get('TWITTER_ACCESS_SECRET')

BASE_URL = base.get('BASE_URL')

ALLOW_SUBSCRIPTIONS = base.get('ALLOW_SUBSCRIPTIONS', False)

FROM_EMAIL = base.get('FROM_EMAIL')