#coding: utf-8

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from cerci_content.models import IssueContent, Author, Genre
from cerci_issue.models import Issue
from django.shortcuts import get_object_or_404
from taggit.models import Tag
import feedparser


def get_issues():
    return Issue.objects.prefetch_related(
        'issue2content_set',
        'issue2content_set__content',
        'issue2content_set__content__genres',
        'issue2content_set__content__authors'
    ).filter(
        is_published=True).order_by('-published_at')


@cache_page(2592000)
def home(request, year=None):
    issues = get_issues()
    return render_to_response(
        'home.html',
        {'issues': issues[1:],
         'last_issue': issues[0]},
        context_instance=RequestContext(request))


def current_issue(request, issue_number):
    key = 'issue_%s' % issue_number
    rendered = cache.get(key)
    user_is_editor = request.user.has_perm('cerci_content.add_issuecontent')
    if rendered and not user_is_editor:
        return HttpResponse(rendered)

    issue = get_object_or_404(Issue.objects.prefetch_related(
        'issue2content_set',
        'issue2content_set__content',
        'issue2content_set__content__genres',
        'issue2content_set__content__authors'
    ), number=issue_number)
    if not user_is_editor and not issue.is_published:
        raise Http404()
    next = None
    contents = issue.get_contents()
    if len(contents):
        next = contents[0].content

    template = get_template('issue.html')
    context = {'issue': issue,
               'next': next}
    request_context = RequestContext(request, context)
    rendered = template.render(request_context)
    if not user_is_editor:
        cache.set(key, rendered, 2592000)
    return HttpResponse(rendered)


def current_issuecontent(request, issue_number, contentslug):
    """
    We should display the content within its related issue. Since a content can
    have multiple issues and an issue can have multiple contents we need a
    unique identifier for issue. In that context it's <issue_number> for the
    sake of short urls.
    """
    preview = False
    key = 'issuecontent_%s_%s' % (issue_number, contentslug)
    rendered = cache.get(key)
    user_is_editor = request.user.has_perm('cerci_content.add_issuecontent')
    if rendered and not user_is_editor:
        return HttpResponse(rendered)

    issuecontent = get_object_or_404(IssueContent.objects.prefetch_related(
        'figures', 'genres', 'authors'
    ), slug=contentslug)
    issue = get_object_or_404(Issue, number=issue_number)
    is_published = issue.is_published and issuecontent.is_published
    if not user_is_editor and not is_published:
        raise Http404
    if user_is_editor and not is_published:
        preview = True
    prev = issuecontent.prev(issue)
    if not prev:
        prev = issue
    next = issuecontent.next(issue)
    template = get_template('issuecontent.html')
    context = {'issue': issue,
               'issuecontent': issuecontent,
               'next': next,
               'prev': prev,
               'preview': preview}
    request_context = RequestContext(request, context)
    rendered = template.render(request_context)
    if not user_is_editor:
        cache.set(key, rendered, 2592000)
    return HttpResponse(rendered)


@cache_page(2592000)
def author_list(request, initial='A'):
    order = u"ABCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜXWVYZ"
    initials = sorted(
        set([i[0] for i in Author.objects.filter(
            is_published=True).values_list('name', flat=True)]),
        key=lambda i: order.index(i) if i in order else 1000)
    authors = Author.objects.filter(is_published=True,
                                    name__startswith=initial).order_by('name')
    return render_to_response('authors.html',
                              {'authors': authors,
                               'initial': initial,
                               'initials': initials},
                              context_instance=RequestContext(request))


def author(request, author_slug):
    def get_page(contents, figures, figure_contents, issue_covers):
        index = {'contents': 0, 'figures': 1, 'figures_used': 2,  'covers': 3}
        all_contents = {'contents': contents,
                        'figures': figures,
                        'figures_used': figure_contents,
                        'covers': issue_covers}
        filtered = filter(lambda x: all_contents[x], all_contents)
        if len(filtered):
            return index.get(filtered[0])
        return

    active = int(request.GET.get('tab', 0))
    key = 'author_%s_%s' % (author_slug, active)
    rendered = cache.get(key)
    user_is_editor = request.user.has_perm('cerci_content.add_issuecontent')
    if rendered and not user_is_editor:
        return HttpResponse(rendered)

    author = get_object_or_404(Author, slug=author_slug)
    if not user_is_editor and not author.is_published:
        raise Http404()

    if author.all_contents or author.covers:
        hascontent = True
        if not author.contents and not request.GET.get('tab'):
            page = get_page(
                author.contents, author.figures,
                author.figure_contents, author.covers) or 'none'
            return HttpResponseRedirect(
                reverse('author',
                        kwargs={
                            'author_slug': author.slug}) + '?tab=%s' % page)
    else:
        hascontent = False

    template = get_template('author.html')
    context = {'author': author,
               'active': active,
               'hascontent': hascontent}
    request_context = RequestContext(request, context)
    rendered = template.render(request_context)
    if not user_is_editor:
        cache.set(key, rendered, 2592000)
    return HttpResponse(rendered)


@cache_page(2592000)
def genre(request, genreslug):
    genre = get_object_or_404(Genre, slug=genreslug)
    contents = genre.issuecontent_set.prefetch_related(
        'figures', 'issue_set', 'authors', 'tags'
    ).filter(
        is_published=True).order_by('-updated_at')
    return render_to_response('category.html',
                              {'title': genre.name,
                               'contents': contents},
                              context_instance=RequestContext(request))


@cache_page(2592000)
def tag(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    contents = IssueContent.objects.prefetch_related(
        'figures', 'issue_set', 'authors', 'tags'
    ).filter(tags__slug=tagslug, is_published=True).order_by('-updated_at')
    return render_to_response('category.html',
                              {'title': tag.name,
                               'contents': contents},
                              context_instance=RequestContext(request))


@cache_page(2592000)
def masterhead(request):
    return render_to_response('masterhead.html',
                              {},
                              context_instance=RequestContext(request))


def blog(request):
    posts = cache.get('blog')
    if not posts:
        posts = feedparser.parse(settings.BLOG_FEED)
        cache.set('blog', posts, timeout=21600)
    return render_to_response('blog.html',
                              {'posts': posts, 'blog_url': settings.BLOG},
                              context_instance=RequestContext(request))


@cache_page(2592000)
def yandex_proof(request):
    return HttpResponse('0d42572b3ba6')
