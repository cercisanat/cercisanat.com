#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.contrib import messages


def send_mail(template, subject, subject_prefix=settings.EMAIL_SUBJECT_PREFIX,
              request=None, **kwargs):
    plaintext = get_template(template + '.txt')
    htmly = get_template(template + '.html')

    d = Context(kwargs['context'])

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    try:
        msg = EmailMultiAlternatives(
            u'%s | %s' % (subject_prefix, subject),
            text_content,
            settings.SERVER_EMAIL,
            kwargs['email'],
            headers={'Reply-To': 'ekip@cercisanat.com'})
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        if request:
            messages.add_message(request, messages.WARNING,
                                 "Couldn't send email.")
            messages.add_message(request, messages.WARNING, str(e))
