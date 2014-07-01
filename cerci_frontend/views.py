from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
from cerci_content.models import IssueContent, Author, Genre
from cerci_issue.models import Issue
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from taggit.models import Tag


def get_issues(year):
    return Issue.objects.prefetch_related(
        'issue2content_set',
        'issue2content_set__content',
        'issue2content_set__content__genres',
        'issue2content_set__content__authors'
    ).filter(
        is_published=True,
        published_at__year=year).order_by('-published_at')


def home(request, year=str(now().year)):
    year = int(year)
    if Issue.objects.filter(is_published=True).exists():
        issues = get_issues(year)
        while not issues.exists():
            year = year - 1
            issues = get_issues(year)

        first = Issue.objects.order_by('published_at').filter(
            is_published=True)
        if first.exists():
            first_year = first[0].published_at.year
            last_year = Issue.objects.filter(
                is_published=True).latest('published_at').published_at.year
            return render_to_response(
                'home.html',
                {'issues': issues, 'year': year,
                 'first_year': first_year, 'last_year': last_year},
                context_instance=RequestContext(request))
    else:
        return render_to_response(
            'nocontent.html',
            {},
            context_instance=RequestContext(request))


def current_issue(request, issue_number):
    issue = get_object_or_404(Issue.objects.prefetch_related(
        'issue2content_set',
        'issue2content_set__content',
        'issue2content_set__content__genres',
        'issue2content_set__content__authors'
    ), number=issue_number)
    return render_to_response('issue.html',
                              {'issue': issue},
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
    next = issuecontent.next(issue)
    if issuecontent.is_figure:
        template = 'issuecontent_figure.html'
    else:
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
    author = get_object_or_404(Author, slug=author_slug, is_published=True)
    return render_to_response('author.html',
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


def yandex_proof(request):
    return HttpResponse('0d42572b3ba6')
