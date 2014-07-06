# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import env, roles, run, sudo
from fabric.context_managers import prefix
from fabric.contrib.project import rsync_project
import os

env.roledefs = {
    'http': [
        '146.185.159.190'
    ]
}

environments = {
    "dev": {
        'code_dir': '/var/sites/cerci/dev',
        'workon': 'cerci_dev'
    },
    "staging": {
        'code_dir': '/var/sites/cerci/staging',
        'workon': 'cerci_staging'
    },
    "prod": {
        'code_dir': '/var/sites/cerci/www',
        'workon': 'cerci'
    }
}


@roles('http')
def restart():
    env.user = 'root'
    sudo('service apache2 reload')


@roles('http')
def deploy(name='dev'):
    env.user = 'cerci'
    if os.path.exists('fabfile.py'):
        rsync_project(
            remote_dir=environments[name]['code_dir'],
            local_dir='./',
            exclude=['.git',
                     'media',
                     '/static',
                     '*.pyc',
                     'cerci/settings_main.py',
                     'cerci/whoosh_index',
                     '/fabfile.py',
                     '/restore',
                     '/get_data',
                     '/get_data_remote_script'])
    else:
        raise Exception('Wrong directory')

    with prefix('source /usr/local/bin/'
                'virtualenvwrapper.sh '
                '&& workon %s' % environments[name]['workon']):
        run('mkdir -p media/ckeditor')
        run('./manage.py collectstatic --noinput')
        run('./manage.py compress')
    restart()
