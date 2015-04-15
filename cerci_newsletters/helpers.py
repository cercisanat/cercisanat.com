from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import render_to_string

from .models import Subscriber, Newsletter, SentItem
from cerci_issue.models import Issue


def send_mass_html_mail(datatuple, fail_silently=False, user=None,
                        password=None, connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


def send_newsletters(request, issue_number, test=False):
    template = 'emails/newsletters.html'
    issue = Issue.objects.get(number=issue_number)
    domain = settings.SITE_URL
    title = render_to_string('emails/title.txt')
    html = render_to_string(template, {'issue': issue, 'domain': domain})
    newsletter = Newsletter(title=title, template=template, issue=issue)
    newsletter.save()
    if test:
        subscribers = Subscriber.objects.filter(is_staff=True)
    else:
        subscribers = Subscriber.objects.all()
    emails = []
    for subscriber in subscribers:
        emails.append(
            (title, title, html, settings.SERVER_EMAIL,
             [subscriber.email]))

    send_mass_html_mail(emails)

    if not test:
        for subscriber in subscribers:
            sent = SentItem(newsletter=newsletter, subscriber=subscriber,
                            sent_at=timezone.now())
            sent.save()
