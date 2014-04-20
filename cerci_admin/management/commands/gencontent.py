#!/usr/bin/env python
#coding:utf-8
from cerci_content.models import Genre, Author, IssueContent
from cerci_issue.models import Issue, Issue2Content
from utils import pypsum
import random
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from cerci_issue.models import Issue
import datetime
from django.utils.timezone import now


class Command(BaseCommand):
    args = '<authors contents issues>'
    help = 'Generates dummy data'


    def handle(self, *args, **options):

        def generate_authors(count):
            self.stdout.write("generating authors\n")
            with open('utils/male.names') as f:
                males = f.readlines()

            with open('utils/female.names') as f:
                females = f.readlines()

            def genauthname(gender):
                name = random.choice(gender).replace('\n', '')
                last = random.choice(gender).replace('\n', '')
                return name + ' ' + last

            def genmale():
                return genauthname(males)

            def genfemale():
                return genauthname(females)

            for i in range(0, count):
                gender = random.choice([males, females])
                name = genauthname(gender)
                Author(name=name, is_published=True).save()
                self.stdout.write('(%s/%s). Author: "%s" created\n' % (i+1, count, name))

        def generate_genres():
            self.stdout.write("generating genres\n")
            genres = ['Çentik', 'Şiir', 'Öykü', 'Hallaç']
            for genre in genres:
                Genre(name=genre).save()
                self.stdout.write('Genre: "%s" created\n' % genre)

        def generate_issuecontent(count):
            self.stdout.write("generating contents\n")
            genres = Genre.objects.filter(active=True)
            authors = Author.objects.filter(is_published=True)
            for i in range(0, count):
                try:
                    title = pypsum.get_lipsum(random.randint(1, 5), 'words', 'no')[0]
                    body = ''.join(pypsum.get_lipsum(random.randint(5, 10), 'paras', 'yes'))
                    author = random.choice(authors)
                    genre = random.choice(genres)
                    ic = IssueContent(title=title, 
                        body=body, 
                        is_published=True)
                    ic.save()
                    ic.authors.add(author)
                    ic.genres.add(genre)
                    self.stdout.write('(%s/%s). Content: "%s" created\n' % (i+1, count, title))
                except Exception as e:
                    print str(e)
                    pass

        def generate_issue(count):
            self.stdout.write("generating issues\n")
            contents = IssueContent.objects.filter(is_published=True)
            for i in range(0, count):
                try:
                    content_count_for_issue = random.randint(5, 15)
                    issuecontents = []
                    for j in range(0, content_count_for_issue):
                        issuecontents.append(random.choice(contents))
                    # i months ago
                    published_at = (now() - datetime.timedelta(i*2*365/12)).date().isoformat()
                    number = abs(i-count+1)
                    subject = pypsum.get_lipsum(random.randint(1, 5), 'words', 'no')[0]
                    editorial_title = pypsum.get_lipsum(random.randint(1, 5), 'words', 'no')[0]
                    editorial = ''.join(pypsum.get_lipsum(random.randint(3, 8), 'paras', 'yes'))
                    copyright_page = ''.join(pypsum.get_lipsum(random.randint(1, 3), 'paras', 'yes'))
                    issue = Issue(number=number,
                        subject=subject,
                        editorial_title=editorial_title,
                        editorial=editorial,
                        copyright_page=copyright_page,
                        is_published=True,
                        published_at=published_at)
                    issue.save()
                    for j, issuecontent in enumerate(set(issuecontents)):
                        i2c = Issue2Content(issue=issue, content=issuecontent, order=j)
                        i2c.save()
                    self.stdout.write('(%s/%s). Issue: %s "%s" created\n' % (i+1, count, number, subject))
                except Exception as e:
                    print str(e)
                    pass


        author_count = int(args[0])
        content_count = int(args[1])
        issue_count = int(args[2])
        generate_authors(author_count)
        generate_genres()
        generate_issuecontent(content_count)
        generate_issue(issue_count)
        