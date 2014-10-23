# coding: utf-8
from fabric.api import task, env
# from unipath import Path
from .helpers import make_environment

import setup
import db
import deploy

# Always run fabric from the repository root dir.
# Path(__file__).parent.parent.chdir()

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


@task
def stage():
	make_environment('staging', 'guilhermelouro.com.br')


@task
def production():
	make_environment('production', 'guilhermelouro.com.br')



def make_environment(name, domain):
    """
    Configure Fabric's environment according our conventions.
    """
    project = domain.partition('.')[0]
    cname = '%s.%s' % (name, domain)
    env.user = project
    env.hosts = [cname]
    env.settings = '%s.settings' % project
    env.PROJECT = Project('~', cname, project)


    env.user = ''
    env.hosts = ''
    env.project = domain.partition('.')[0]
    env.environment = name
    env.home = ''
    env.local_path = ''
    env.server_path = ''
    env.manage = os.path.join('~/www',env.project,'manage.py')
    env.activate = os.path.join('~/env',env.project,'bin','activate')

    # Requirements path
    env.requirements = os.path.join(env.server_path, 'requirements.txt')


    
    