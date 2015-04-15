from django import forms

from .models import Subscriber


class SubscribeForm(forms.ModelForm):
    class Meta:
        exclude = ['is_staff']
        model = Subscriber
