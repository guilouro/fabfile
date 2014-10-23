# coding: utf-8
from fabric.api import task, env
from .helpers import make_environment
import os

#tasks
import db
import setup
import deploy


RSYNC_EXCLUDE = [
    '*.db',
    '*.pyc',
    '*.sqlite3',
    '.git*',
    '.sass-cache',
    'media/*',
    'tests/*',
    'static/sass',
    'DS_Store',
    'pylintrc',
    'fabfile.py',
    'config.rb',
    'settings/production.py',
    '.ropeproject',
]

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


@task
def production():
    make_environment('production', 'guilhermelouro.com.br')


def config():
    env.project_local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env.project_server_path = os.path.join(env.projserver, env.project)

    env.manage = os.path.join(env.projserver,env.project,'manage.py')
    env.activate = os.path.join(env.envserver,env.project,'bin','activate')

    # Requirements
    env.requirements = os.path.join(env.project_server_path, 'requirements.txt')
    
    




def make_environment(environment, user, hosts, domain):
    """
    Configure Fabric's environment according our conventions.
    """