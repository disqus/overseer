"""
overseer.admin
~~~~~~~~~~~~~~

:copyright: (c) 2011 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from django import forms
from django.contrib import admin

from overseer import conf
from overseer.models import Service, Event, EventUpdate, Subscription

class SubscriptionInline(admin.StackedInline):
    model = Subscription.services.through
    extra = 1

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'order', 'date_updated')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubscriptionInline]

class EventForm(forms.ModelForm):
    if conf.TWITTER_ACCESS_TOKEN and conf.TWITTER_ACCESS_SECRET:
        post_to_twitter = forms.BooleanField(required=False, label="Post to Twitter", help_text="This will send a tweet with a brief summary, the permalink to the event (if BASE_URL is defined), and the hashtag of #status for EACH update you add below.")

    class Meta:
        model = EventUpdate

class EventUpdateInline(admin.StackedInline):
    model = EventUpdate
    extra = 1

class EventAdmin(admin.ModelAdmin):
    form = EventForm
    list_display = ('date_created', 'description', 'status', 'date_updated')
    search_fields = ('description', 'message')
    list_filter = ('services',)
    inlines = [EventUpdateInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save()
        if 'post_to_twitter' in form.cleaned_data and form.cleaned_data['post_to_twitter']:
            for obj in instances:
                obj.event.post_to_twitter(obj.get_message())

class EventUpdateAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'message', 'status', 'event')
    search_fields = ('message',)

class SubscriptionAdmin(admin.ModelAdmin):
    fields = ('email', 'services',)

admin.site.register(Service, ServiceAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventUpdate, EventUpdateAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
