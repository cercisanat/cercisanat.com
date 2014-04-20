from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext as _


class Subscriber(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name=_('Name'))
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=now(), editable=False,
                                      verbose_name=_('Created At'))
    updated_at = models.DateTimeField(editable=False,
                                      verbose_name=_('Updated At'))

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Subscriber, self).save(*args, **kwargs)


class UnsubscribeToken(models.Model):
    subscriber = models.ForeignKey(Subscriber, verbose_name=_('Subscriber'),
                                   unique=True)
    token = models.CharField(max_length=16, verbose_name=_('Token'))
    created_at = models.DateTimeField(default=now(), editable=False,
                                      verbose_name=_('Created At'))
    updated_at = models.DateTimeField(editable=False,
                                      verbose_name=_('Updated At'))

    def __unicode__(self):
        return self.token

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(UnsubscribeToken, self).save(*args, **kwargs)


class Newsletter(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    body = models.TextField(verbose_name=_('Body'))

    created_at = models.DateTimeField(default=now(), editable=False,
                                      verbose_name=_('Created At'))
    updated_at = models.DateTimeField(editable=False,
                                      verbose_name=_('Updated At'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Subscriber, self).save(*args, **kwargs)


class SentItem(models.Model):
    newsletter = models.ForeignKey(Newsletter, verbose_name=_('Newsletter'))
    subscriber = models.ForeignKey(
        Subscriber, related_name='sent_to',
        verbose_name=_('Subscriber'))
    sent_at = models.DateTimeField(verbose_name=_('Sent At'))

    def __unicode__(self):
        return '%s is sent to %s at %s' % (
            self.newsletter.title, self.subscriber.email, self.sent_at)

    class Meta:
        unique_together = ('newsletter', 'subscriber', )
