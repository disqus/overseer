from django.core import mail
from django.test import TestCase

from overseer import conf
from overseer.models import Service, Event, EventUpdate, Subscription

class OverseerTestCase(TestCase):
    urls = 'overseer.tests.urls'
    
    def setUp(self):
        self.service = Service.objects.create(
            name='Test',
            slug='test',
        )
        conf.FROM_EMAIL = 'foo@example.com'
        conf.BASE_URL = 'http://example.com'
    
    def refresh(self, inst):
        return inst.__class__.objects.get(pk=inst.pk)

    def test_subscriptions(self):
        conf.ALLOW_SUBSCRIPTIONS = True
        
        sub = Subscription.objects.create(
            email='foo@example.com',
        )
        sub.services = [self.service]
        
        event = Event.objects.create()
        event.services.add(self.service)
        
        EventUpdate.objects.create(
            event=event,
            status=2,
        )
    
        self.assertEquals(len(mail.outbox), 1)

        msg = mail.outbox[0]

        self.assertEquals(len(msg.to), 1)
        self.assertEquals(msg.to[0], 'foo@example.com')

        body = msg.body

        self.assertTrue('Test may be unavailable' in body)
        self.assertTrue('http://example.com/subscription/%s/' % sub.ident in body)
        
        conf.ALLOW_SUBSCRIPTIONS = False

    def test_cascading_saves(self):
        event = Event.objects.create()
        event.services.add(self.service)
        
        service = self.refresh(self.service)
        
        self.assertEquals(service.status, 0)
        self.assertEquals(event.status, 0)
        self.assertEquals(service.date_updated, event.date_updated)
        
        update = EventUpdate.objects.create(
            event=event,
            status=2,
            message='holy omg wtf',
        )
        
        service = self.refresh(self.service)
        event = self.refresh(event)
        
        self.assertEquals(service.status, update.status)
        self.assertEquals(event.status, update.status)
        self.assertEquals(event.description, update.message)
        self.assertEquals(event.message, update.message)
        self.assertEquals(event.date_updated, update.date_created)
        self.assertEquals(service.date_updated, update.date_created)
