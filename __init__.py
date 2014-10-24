# coding: utf-8
import os
from fabric.api import task, env, require, prefix, run



# Tasks
import deploy
import db
import setup
import gunicorn


@task
def stage():
    env.environment = 'staging'

    # Connection
    env.user = 'guilouro'
    env.hosts = ['guilhermelouro.com.br',]
    env.project = 'GuiSite'
    _config()


@task
def production():
    env.environment = 'production'

    # Connection
    env.user = ''
    env.hosts = ['',]
    env.project = ''
    _config()


def _config():
    
    # Virtualenv server folder
    env.envserver = '~/env' 
    # Folder of all projects on the server
    env.projserver = '~/Projects'

    # Gunicorn
    env.gunicorn_wsgi_app = 'guilouro.wsgi:application'
    env.gunicorn_pidfile = '/tmp/gunicorn_%(project)s.pid' %env
    env.gunicorn_bind = '127.0.0.1:9000'
    env.django_settings_module = 'guilouro.settings'


    # Local and Server Paths
    env.project_local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env.project_server_path = os.path.join(env.projserver, env.project)

    # Vitualenv paths
    env.virtualenv = os.path.join(env.envserver, env.project)
    env.manage = os.path.join(env.projserver,env.project,'manage.py')
    env.activate = os.path.join(env.envserver,env.project,'bin','activate')

    # Requirements
    env.requirements = os.path.join(env.project_server_path, 'requirements.txt')

    

@task
def bootstrap():
    """
    :: Initialize remote host environment.
    """
    require('project', provided_by=('staging', 'production'))

    # Create virtualenv to wrap the environment
    setup.virtualenv()
    # Send the project to the remote host
    deploy.send()
    # Install dependencies on the virtualenv
    setup.requirements()
    # Execute collectstatic
    deploy.collectstatic()
    # Create the database
    db.syncdb()
    # Start gunicorn
    gunicorn.start()