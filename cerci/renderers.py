#coding:utf-8
from django.core.urlresolvers import reverse
from django_medusa.renderers import StaticSiteRenderer
from cerci_issue.models import (Issue, Author)
from cerci_content.models import (IssueContent, Genre)
from taggit.models import Tag


class HomeRenderer(StaticSiteRenderer):
    def get_paths(self):
        return frozenset([
            "/",
        ])


class IssueRenderer(StaticSiteRenderer):
    def get_paths(self):
        paths = set()

        issues = Issue.objects.filter(is_published=True).order_by(
            '-published_at')
        for issue in issues:
            paths.add(reverse('current_issue', args=(issue.number, )))

        issuecontents = IssueContent.objects.prefetch_related(
            'issue_set').filter(is_published=True)
        for issuecontent in issuecontents:
            if issuecontent.issue_set.exists():
                paths.add(reverse('current_issuecontent', args=(
                    issuecontent.issue_set.all()[0].number,
                    issuecontent.slug)))

        return list(paths)


class AuthorRenderer(StaticSiteRenderer):
    def get_paths(self):
        paths = set()

        paths.add(reverse('author_list'))

        initials = u"ABCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜXWVYZ"
        for initial in initials:
            paths.add(reverse('author_list', args=(initial,)))

        authors = Author.objects.filter(is_published=True)

        for author in authors:
            paths.add(reverse('author', args=(author.slug,)))
        return list(paths)


class GenreRenderer(StaticSiteRenderer):
    def get_paths(self):
        paths = set()

        genres = Genre.objects.all()

        for genre in genres:
            paths.add(reverse('genre', args=(genre.slug,)))
        return list(paths)


class TagRenderer(StaticSiteRenderer):
    def get_paths(self):
        paths = set()

        tags = Tag.objects.all()

        for tag in tags:
            paths.add(reverse('tag', args=(tag.slug,)))
        return list(paths)


class StaticPagesRenderer(StaticSiteRenderer):
    def get_paths(self):
        paths = ['crew', 'manifest', 'sendus', 'rules', 'contact']
        return [reverse(i) for i in paths]


renderers = [HomeRenderer, IssueRenderer, AuthorRenderer,
             StaticPagesRenderer, TagRenderer, GenreRenderer]
