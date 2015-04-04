from django import forms

from .models import Subscriber


class SubscribeForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = Subscriber
