from django.conf import settings
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.core.cache import cache
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


def home(request):
    issues = get_issues()
    return render_to_response(
        'home.html',
        {'issues': issues[1:],
         'last_issue': issues[0]},
        context_instance=RequestContext(request))


def current_issue(request, issue_number):
    issue = get_object_or_404(Issue.objects.prefetch_related(
        'issue2content_set',
        'issue2content_set__content',
        'issue2content_set__content__genres',
        'issue2content_set__content__authors'
    ), number=issue_number)
    next = issue.get_contents()[0].content
    return render_to_response('issue.html',
                              {'issue': issue,
                               'next': next},
                              context_instance=RequestContext(request))


def current_issuecontent(request, issue_number, contentslug):
    """
    We should display the content within its related issue. Since a content can
    have multiple issues and an issue can have multiple contents we need a
    unique identifier for issue. In that context it's <issue_number> for the
    sake of short urls.
    """
    preview = False
    issuecontent = get_object_or_404(IssueContent.objects.prefetch_related(
        'figures', 'genres', 'authors'
    ), slug=contentslug)
    issue = get_object_or_404(Issue, number=issue_number)
    if not request.user.has_perm('cerci_content.add_issuecontent') and \
       (not issue.is_published or not issuecontent.is_published):
        raise Http404
    if request.user.has_perm('cerci_content.add_issuecontent') and \
       (not issue.is_published or not issuecontent.is_published):
        preview = True
    prev = issuecontent.prev(issue)
    if not prev:
        prev = issue
    next = issuecontent.next(issue)
    template = 'issuecontent.html'
    return render_to_response(template,
                              {'issue': issue,
                               'issuecontent': issuecontent,
                               'next': next,
                               'prev': prev,
                               'preview': preview},
                              context_instance=RequestContext(request))


def author_list(request):
    authors = Author.objects.filter(is_published=True).order_by('name')
    return render_to_response('authors.html',
                              {'authors': authors},
                              context_instance=RequestContext(request))


def author(request, author_slug):
    def get_page(contents, figure_contents, issue_covers):
        all_contents = {'contents': contents,
                        'illustrations': figure_contents,
                        'covers': issue_covers}
        filtered = filter(lambda x: all_contents[x], all_contents)
        if len(filtered):
            return filtered[0]

    author = get_object_or_404(Author, slug=author_slug, is_published=True)
    illustrations = request.GET.get('illustrations')
    covers = request.GET.get('covers')
    template = 'author.html'
    if illustrations:
        template = 'author_illustrations.html'
    if covers:
        template = 'author_covers.html'
    if not author.contents and not covers and not illustrations:
        page = get_page(author.contents, author.figure_contents, author.covers)
        return HttpResponseRedirect(
            reverse('author',
                    kwargs={'author_slug': author.slug}) + '?' + page + '=1')

    return render_to_response(template,
                              {'author': author},
                              context_instance=RequestContext(request))


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


def tag(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    contents = IssueContent.objects.prefetch_related(
        'figures', 'issue_set', 'authors', 'tags'
    ).filter(tags__slug=tagslug, is_published=True).order_by('-updated_at')
    return render_to_response('category.html',
                              {'title': tag.name,
                               'contents': contents},
                              context_instance=RequestContext(request))


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


def yandex_proof(request):
    return HttpResponse('0d42572b3ba6')
