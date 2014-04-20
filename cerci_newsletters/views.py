from ajax_forms.views import AjaxModelFormView

from .forms import SubscribeForm
from .models import Subscriber


class SubscribeFormView(AjaxModelFormView):
    template_name = "subscribe-form.html"
    form_class = SubscribeForm
    model = Subscriber

    def valid_submit(self, form):
        """Send an email here"""
        pass
