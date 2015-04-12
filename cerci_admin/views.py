from cerci_issue.models import Issue, IssueContent
from django.core.cache import cache
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.admin.views.decorators import staff_member_required
from easy_thumbnails.files import get_thumbnailer
from django.http import HttpResponse, HttpResponseRedirect


@staff_member_required
def publish_issue(request, issue_id):
    issue = Issue.objects.get(pk=issue_id)
    issue.is_published = True
    issue.save()
    for content in issue.contents.all():
        content.is_published = True
        for figure in content.figures.all():
            figure.is_published = True
            figure.save()
        content.save()
    cache.clear()
    messages.add_message(
        request,
        messages.SUCCESS,
        _("This issue is now published and visible for visitors."))
    return redirect('admin:cerci_issue_issue_change', issue_id)


@staff_member_required
def unpublish_issue(request, issue_id):
    issue = Issue.objects.get(pk=issue_id)
    issue.is_published = False
    issue.save()
    for content in issue.contents.all():
        content.is_published = False
        for figure in content.figures.all():
            figure.is_published = False
            figure.save()
        content.save()
    messages.add_message(
        request,
        messages.WARNING,
        _("Notice: You have just unpublished an issue!"))
    return redirect('admin:cerci_issue_issue_change', issue_id)


@staff_member_required
def thumbnail_by_id(request, id):
    figure = IssueContent.objects.get(pk=id)
    thumbnail = get_thumbnailer(figure.image).get_thumbnail(
        {'size': (50, 50)})
    thumbnail.open()
    return HttpResponse(thumbnail.read(), content_type="image/jpeg")


@staff_member_required
def clear_cache(request):
    next = request.GET.get('next', '/')
    cache.clear()
    messages.add_message(
        request,
        messages.SUCCESS,
        _("Cache cleared"))
    return HttpResponseRedirect(next)
