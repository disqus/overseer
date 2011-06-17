"""
overseer.templatetags.overseer_helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2011 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import datetime

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def timesince(value):
    from django.template.defaultfilters import timesince
    if not value:
        return 'Never'
    if value < datetime.datetime.now() - datetime.timedelta(days=5):
        return value.date()
    value = (' '.join(timesince(value).split(' ')[0:2])).strip(',')
    if value == '0 minutes':
        return 'Just now'
    if value == '1 day':
        return 'Yesterday'
    return value + ' ago'

@register.filter(name='truncatechars')
@stringfilter
def truncatechars(value, arg):
    """
    Truncates a string after a certain number of chars.

    Argument: Number of chars to truncate after.
    """
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int().
        return value # Fail silently.
    if len(value) > length:
        return value[:length] + '...'
    return value
truncatechars.is_safe = True

@register.filter
def duration(value):
    if isinstance(value, datetime.timedelta):
        value = value.days * 24 * 3600 + value.seconds
    hours, minutes, seconds = 0, 0, 0
    if value > 3600:
        hours = value / 3600
        value = value % 3600
    if value > 60:
        minutes = value / 60
        value = value % 60
    seconds = value
    if hours:
        return '%s hours' % (hours,)
    if minutes:
        return '%s minutes' % (minutes,)
    if seconds:
        return '%s seconds' % (seconds,)
    return 'n/a'