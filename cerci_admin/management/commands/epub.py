#!/usr/bin/env python
#coding:utf-8
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from cerci_issue.models import Issue
import os
import shutil
from bs4 import BeautifulSoup
from django.core.files.storage import default_storage
import sys
from xml.dom.minidom import parse, parseString
import codecs
import string
import mimetypes


def translate_non_alphanumerics(to_translate, translate_to=u''):
    not_letters_or_digits = string.punctuation.replace('_', '').replace('-', '')
    translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
    return to_translate.translate(translate_table)

def generate_manifest(path):
    pwd = os.getcwd()
    os.chdir(path)
    try:
        container = parse(os.path.join(path, 'META-INF/container.xml'))
    except IOError:
        raise Exception('container.xml not found in specified path')
    ops_path = container.getElementsByTagName("rootfiles")[0]\
                .getElementsByTagName("rootfile")[0].attributes['full-path'].value

    manifest = parseString('<manifest></manifest>')

    mimetypes.add_type('application/vnd.ms-opentype', '.ttf', True)
    mimetypes.add_type('application/vnd.ms-opentype', '.otf', True)
    mimetypes.add_type('application/font-woff', '.wof', True)

    excluded_files = ['package.opf']
    special_files = {'toc.xhtml': {'properties': 'nav'}}

    output = ''
    for root, dirs, files in os.walk(os.path.join(path.decode('utf-8'), os.path.dirname(ops_path))):
        for filename in files:
            relpath = os.path.relpath(os.path.join(root, filename), os.path.dirname(ops_path))
            html_id = translate_non_alphanumerics(relpath.replace('/', '__').replace(' ', ''))
            mimetype = mimetypes.guess_type(relpath)
            if mimetype[0]:
                if not relpath in excluded_files:
                    item = manifest.createElement('item')
                    item.setAttribute('id', html_id)
                    item.setAttribute('href', relpath)
                    item.setAttribute('media-type', mimetype[0])
                    if relpath in special_files:
                        for attr in special_files[relpath]:
                            item.setAttribute(attr, special_files[relpath][attr])
                    output += item.toxml() + '\n'
    os.chdir(pwd)
    return output

def generate_spine(spine):
    output = ''
    for item in spine:
        output += '<itemref idref="%s"/>\n' % item.replace('.', '')
    return output


def generate_toc(spine):
    output = ''
    for item in spine:
        output += '<li><a href="%s">T</a></li>\n' % item
    return output


class Command(BaseCommand):
    args = '<issue_number>'
    help = 'Generates an epub file whish is most probably invalid'


    def handle(self, *args, **options):
        issue_number = args[0]
        issue = Issue.objects.get(number=issue_number)
        issuecontents = issue.get_contents()
        
        skeleton_path = os.path.join(os.path.dirname(__file__), 'epub-skeleton')
        epub_files_root = os.path.join(settings.MEDIA_ROOT, 'epubs')
        path = os.path.join(epub_files_root, '%s-%s' % (issue_number, issue.slug))
        OPS = os.path.join(path, 'container', 'OPS')
        if not os.path.exists(epub_files_root):
            os.mkdir(epub_files_root)
        
        if os.path.exists(path):
            shutil.rmtree(path)
        shutil.copytree(skeleton_path, path)
        
        template = get_template('epub/content.xhtml')
        spine = []
        for counter, issuecontent in enumerate(issuecontents):
            xhtml = template.render(Context({'issue': issue, 'issuecontent': issuecontent.content}))
            soup = BeautifulSoup(xhtml)
            
            # save inline images added by ckeditor
            for image in soup.findAll('img'):
                image_src = image.get('src')
                if image_src.startswith('/media/ckeditor/'):
                    image_src_path = image_src.replace('/media/', '')
                    image_src_output = image_src.replace('/media/ckeditor/', 'images/').replace(' ', '')
                    image_dirname = os.path.dirname(image_src_output)
                    if not os.path.exists(os.path.join(OPS, image_dirname )):
                        os.makedirs(os.path.join(OPS, image_dirname ))
                    if default_storage.exists(image_src_path):
                        with default_storage.open(image_src_path, 'r') as input_file:
                            with open(os.path.join(OPS, image_src_output), 'w') as output_file:
                                output_file.write(input_file.read())
                    image.attrs['src'] = image_src_output
            
            # save content images (figures)
            figures = issuecontent.content.figures.all()
            if figures.count():
                image_src = figures[0].image.url
                image_src_path = figures[0].image.path
                image_src_output = image_src.replace('/media/', '').replace(' ', '')
                image_dirname = os.path.dirname(image_src_output)
                if not os.path.exists(os.path.join(OPS, image_dirname )):
                    os.makedirs(os.path.join(OPS, image_dirname ))
                if default_storage.exists(image_src_path):
                    with default_storage.open(image_src_path, 'r') as input_file:
                        with open(os.path.join(OPS, image_src_output), 'w') as output_file:
                            output_file.write(input_file.read())
            
            xhtml = soup.prettify()
            filename = 'article-%s.xhtml'%(counter+1)
            spine.append(filename)
            with open(os.path.join(OPS, 'article-%s.xhtml'%(counter+1)), 'w') as f:
                f.write(xhtml.encode('utf8'))


        # create toc.xhtml
        template = get_template('epub/toc.xhtml')
        generated_toc = generate_toc(spine)
        tocxhtml = template.render(Context({'issue': issue, 
                                           'generated_toc': generated_toc}))
        soup = BeautifulSoup(tocxhtml)
        tocxhtml = soup.prettify()
        with open(os.path.join(OPS, 'toc.xhtml'), 'w') as f:
            f.write(tocxhtml.encode('utf8'))

        # generate package.opf
        generated_manifest = generate_manifest(os.path.join(path, 'container'))
        generated_spine = generate_spine(spine)
        
        template = get_template('epub/package.opf')
        package_opf = template.render(Context({'issue': issue, 
                                               'generated_manifest': generated_manifest,
                                               'generated_spine': generated_spine}))
        soup = BeautifulSoup(package_opf)
        package_opf = soup.prettify()
        with open(os.path.join(OPS, 'package.opf'), 'w') as f:
            f.write(package_opf.encode('utf8'))
            
