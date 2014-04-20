"""
WSGI config for cerci project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import site
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cerci.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import newrelic.agent

NEWRELIC_INI_FILE = os.path.join(settings.PROJECT_ROOT, 'newrelic.ini')
if os.path.exists(NEWRELIC_INI_FILE):
    newrelic.agent.initialize(NEWRELIC_INI_FILE)
    application = newrelic.agent.WSGIApplicationWrapper(application)
