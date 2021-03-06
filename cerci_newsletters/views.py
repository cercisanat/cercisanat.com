import urllib

from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from ajax_forms.views import AjaxModelFormView

from .forms import SubscribeForm
from .models import Subscriber, UnsubscribeToken
from .utils import mailer
from .utils.generators import generate_unsubscribe_token
from .helpers import send_newsletters

from cerci_issue.models import Issue


class SubscribeFormView(AjaxModelFormView):
    template_name = "newsletters/subscribe-form.html"
    form_class = SubscribeForm
    model = Subscriber

    def valid_submit(self, form):
        """Send an email here"""
        pass


class UnsubscribeView(TemplateView):
    template_name = "newsletters/unsubscribe.html"

    def get_context_data(self, **kwargs):
        context = super(UnsubscribeView, self).get_context_data(**kwargs)
        self.email = self.request.GET.get('email')
        if self.email:
            self.email = urllib.unquote_plus(self.email)
            context['email'] = self.email
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        t = self.request.GET.get('token')
        if t:
            unsubscribe_token = get_object_or_404(UnsubscribeToken, token=t)
            unsubscribe_token.subscriber.delete()
            context['unsubscribed'] = True
            return self.render_to_response(context)
        else:
            if self.email:
                subscriber = get_object_or_404(Subscriber, email=self.email)
                try:
                    unsubscribe_token = UnsubscribeToken.objects.get(
                        subscriber=subscriber)
                    t = unsubscribe_token.token
                except UnsubscribeToken.DoesNotExist:
                    t = generate_unsubscribe_token()
                    unsubscribe_token = UnsubscribeToken(subscriber=subscriber,
                                                         token=t)
                unsubscribe_token.save()
                unsubscribe_link = (settings.SITE_URL +
                                    reverse('unsubscribe') +
                                    '?token=' + t)
                mailer.send_mail(
                    request=request,
                    template='newsletters/email/unsubscribe',
                    subject=u'unsubscribe',
                    context={'unsubscribe_link': unsubscribe_link},
                    email=[self.email])
            return self.render_to_response(context)


@staff_member_required
def email_template_debug(request, issue_number):
    issue = Issue.objects.get(number=issue_number)
    domain = settings.SITE_URL
    return render_to_response('emails/newsletters.html',
                              {'issue': issue,
                               'domain': domain},
                              context_instance=RequestContext(request))


@staff_member_required
def test_sending(request, issue_number):
    send_newsletters(request, issue_number, test=True)
    messages.success(request, 'Test Newsletters sent')
    return HttpResponseRedirect(request.GET.get('next', '/'))


@staff_member_required
def send(request, issue_number):
    send_newsletters(request, issue_number)
    messages.success(request, 'Newsletters sent')
    return HttpResponseRedirect(request.GET.get('next', '/'))
