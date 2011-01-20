"""
A service's status should be:

- red if any(updates affecting service) are red
- yellow if any(updates affecting service) are yellow
- green if all(updates affecting service) are green
"""

from django.db import models
from django.db.models.signals import post_save

import datetime

STATUS_CHOICES = (
    (0, 'No Problems'),
    (1, 'Some Issues'),
    (2, 'Unavailable'),
)

class Service(models.Model):
    """
    A ``Service`` can describe any part of your architecture. Each 
    service can have many events, in which the last event should be shown
    (unless the status is 'No Problems').
    """
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    order = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    date_updated = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        ordering = ('order', 'name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.date_updated = datetime.datetime.now()
        super(Service, self).save(*args, **kwargs)

    @classmethod
    def handle_event_save(cls, instance, created, **kwargs):
        for service in instance.services.all():
            update_qs = Service.objects.filter(pk=service.pk)
            if instance.date_updated > service.date_updated:
                # If the update is newer than the last update to the service
                update_qs.filter(date_updated__lt=instance.date_updated)\
                         .update(date_updated=instance.date_updated)

            if instance.status > service.status:
                # If our status more critical (higher) than the current
                # service status, update to match the current
                update_qs.filter(status__lt=instance.status)\
                         .update(status=instance.status)
            elif instance.status < service.status:
                # If no more events match the current service status, let's update
                # it to the current status
                if not Event.objects.filter(services=service, status=service.status)\
                                    .exclude(pk=instance.pk).exists():
                    update_qs.filter(status__gt=instance.status)\
                             .update(status=instance.status)

class Event(models.Model):
    """
    An ``Event`` is a collection of updates related to one event.
    
    - ``message`` stores the last message from ``StatusUpdate`` for this event.
    """
    services = models.ManyToManyField(Service)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    message = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    date_updated = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u"%s on %s" % (self.date_created, '; '.join(self.services.values_list('name', flat=True)))

    @classmethod
    def handle_update_save(cls, instance, created, **kwargs):
        event = instance.event

        if created:
            is_latest = True
        elif EventUpdate.objects.filter(event=event).order_by('-date_created')\
                                .values_list('event', flat=True)[0] == event.pk:
            is_latest = True
        else:
            is_latest = False

        if is_latest:
            Event.objects.filter(pk=event.pk).update(
                status=instance.status,
                message=instance.message,
                date_updated=instance.date_created,
            )
            event.status = instance.status
            event.message = instance.message
            event.date_updated = instance.date_created
            post_save.send(sender=Event, instance=event, created=False)

class EventUpdate(models.Model):
    """
    An ``EventUpdate`` contains a single update to an ``Event``. The latest update
    will always be reflected within the event, carrying over it's ``status`` and ``message``.
    """
    event = models.ForeignKey(Event)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    message = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return unicode(self.date_created)

post_save.connect(Service.handle_event_save, sender=Event)
post_save.connect(Event.handle_update_save, sender=EventUpdate)
