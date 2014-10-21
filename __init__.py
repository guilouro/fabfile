from fabric import colors
from fabric.utils import puts
from fabric.api import run, require, env
from fabric.context_managers import prefix
from fabric.contrib.project import rsync_project
import os
# import fabric_gunicorn as gunicorn

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


env.project = 'Blog'
env.python_version = 'python2.7'
env.local_root_path = os.path.abspath(os.path.dirname(__file__))



def _paths():
    env.home = os.path.join(env.root, env.project)
    env.project_root_path = env.home
    
    # Manage file
    env.manage_file = os.path.join(env.project_root_path, 'manage.py')
    
    # Http paths
    # env.static_path = os.path.join(env.root, '%s_static' % env.project)
    # env.apache_conf = os.path.join(env.home, 'apache2', 'conf',
    #    '%s.conf' % env.project)
    # env.cgi_file = os.path.join(env.home, 'dispatch.wsgi')
    
    # Virtualenv paths
    env.virtualenv_root = os.path.join("~/env", env.project)
    env.virtualenv_activate = os.path.join(env.virtualenv_root, 'bin',
        'activate')
    
    # Requirements path
    env.requirements = os.path.join(env.project_root_path, 'requirements.txt')
    



def staging():
    """
    Use staging environment on remote host.
    """
    env.environment = 'staging'
    env.python_version = 'python2.7'

    # Remote settings
    env.user = 'vagrant'
    env.hosts = ['10.0.0.100', ]
    env.password = 'vagrant'

    # Paths
    env.root = os.path.join('/home', 'vagrant', 'www')
    _paths()



def lista():
    # print env.local_root_path + "/"
    run("ls -la")



def create_virtualenv():
    """
    Setup virtualenv on remote host.
    """
    require('project', provided_by=('staging', 'production'))

    with prefix("export PROJECT_HOME=$HOME/www"):
        with prefix("export WORKON_HOME=$HOME/env"):
            with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                run("mkproject %(project)s" % env)
    

def update_requirements():
    """
    Update Python dependencies on remote host.
    """
    with prefix("export PROJECT_HOME=$HOME/www"):
        with prefix("export WORKON_HOME=$HOME/env"):
            with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                run("workon %(project)s; pip install -r %(requirements)s; deactivate" % env)


def syncdb():
    """
    Execute syncdb on remote host.
    """
    require('virtualenv_activate', provided_by=('staging', 'production'))

    run(('source %(virtualenv_activate)s; python %(manage_file)s '
        ' syncdb') % env)


def deploy():
    """
    Send the code to the remote host.
    """
    require('home', provided_by=('staging', 'production'))

    # Copy the project
    rsync_project(
        remote_dir=env.home,
        local_dir=env.local_root_path + "/",
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts='--omit-dir-times',
    )


#TODO
def up_gunicorn():
    """ 
    Up gunicorn
    """
    require('virtualenv_activate', provided_by=('staging', 'production'))
    run('source ~/env/Django/bin/activate && ~/env/Django/bin/gunicorn -w3 Teste.wsgi:application --bind 10.0.0.100:5000 --pid /tmp/gunicorn_Teste.pid -D')
    # run('source ~/env/Django/bin/activate; pip freeze')


def collect_static():
    """
    Collect all static files from Django apps and copy them into the public
    static folder.
    """
    require('project_root_path', provided_by=('staging', 'production'))
    run(('source %(virtualenv_activate)s; '
            'python %(manage_file)s collectstatic; '
            'deactivate') % env,
    )



def bootstrap():
    """
    Initialize remote host environment.
    """
    require('root', provided_by=('staging', 'production'))

    # Create virtualenv to wrap the environment
    create_virtualenv()
    # Send the project to the remote host
    deploy()
    # Install dependencies on the virtualenv
    update_requirements()
    # Create the database
    syncdb()




