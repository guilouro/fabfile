# coding: utf-8
from fabric.api import task, env, require
from .helpers import make_environment
import os

#tasks
import deploy
import db
import setup


# Virtualenv server folder
env.envserver = '~/env' 
# Folder of all projects on the server
env.projserver = '~/Projects'



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
    env.user = 'guilouro'
    env.hosts = ['guilhermelouro.com.br',]
    env.project = 'GuiSite'
    _config()


def _config():
    env.project_local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env.project_server_path = os.path.join(env.projserver, env.project)

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
    # Create the database
    db.syncdb()