from django.core.management.base import BaseCommand
from django.conf import settings
import os
import subprocess
from cerci_issue.models import *
import shutil

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        command = """wget -nH -r -p -e robots=off --exclude-directories=static,media,__debug__ http://localhost:8000"""
        os.chdir(settings.DEPLOY_PATH)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print process.returncode
        
        issues = Issue.objects.filter(is_published=True)
        for issue in issues:
            os.chdir(os.path.join(settings.DEPLOY_PATH, 'dergi', str(issue.number)))
            command = """wget http://localhost:8000/dergi/%s""" % issue.number
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            print process.returncode
            os.rename(str(issue.number), 'index.html')
            
        os.chdir(settings.DEPLOY_PATH)
        if os.path.exists('static'):
            shutil.rmtree('static')
        shutil.copytree(os.path.join(settings.PROJECT_ROOT, 'static'), 'static')
        print "static files copied"
        
        if os.path.exists('media'):
            shutil.rmtree('media')
        shutil.copytree(os.path.join(settings.PROJECT_ROOT, 'media'), 'media')
        print "media files copied"
        #self.stdout.write(process.returncode)
