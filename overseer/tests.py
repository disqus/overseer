from django.test import TestCase

from overseer.models import Service, Event, EventUpdate

class OverseerTestCase(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Test',
            slug='test',
        )
    
    def refresh(self, inst):
        return inst.__class__.objects.get(pk=inst.pk)

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