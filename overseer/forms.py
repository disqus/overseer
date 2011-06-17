"""
overseer.forms
~~~~~~~~~~~~~~

:copyright: (c) 2011 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from django import forms

from overseer.models import Service, Subscription, UnverifiedSubscription

class BaseSubscriptionForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        fields = ('services',)
        model = Subscription

class NewSubscriptionForm(BaseSubscriptionForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'you@example.com'}))
    
    class Meta:
        fields = ('email', 'services',)
        model = UnverifiedSubscription

    def clean_email(self):
        value = self.cleaned_data.get('email')
        if value:
            value = value.lower()
        return value            

class UpdateSubscriptionForm(BaseSubscriptionForm):
    unsubscribe = forms.BooleanField(required=False)
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
