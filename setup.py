# coding: utf-8
from fabric.colors import red
from fabric.api import env, require, run, task, cd
from fabric.context_managers import prefix
from fabric.contrib.files import exists


@task
def lista():
	"""
	:: List home
	"""
	run('ls -la')


@task
def virtualenv():
    """
    :: Setup virtualenv on remote host.
    """
    require('project', provided_by=('staging', 'production'))

    with prefix("export PROJECT_HOME=%(projserver)s" %env):
        with prefix("export WORKON_HOME=%(envserver)s" %env):
            with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                run("mkproject %(project)s" % env)


@task
def requirements():
    """
    :: Update Python dependencies on remote host.
    """
    require('project', provided_by=('staging', 'production'))

    with prefix("export PROJECT_HOME=%(projserver)s" %env):
        with prefix("export WORKON_HOME=%(envserver)s" %env):
            with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                run("workon %(project)s; pip install -r %(requirements)s; deactivate" % env)

@task
def del_app():
    """
    :: Delete project
    """
    require('project', provided_by=('staging', 'production'))

    with cd(env.projserver):
        with prefix("export PROJECT_HOME=%(projserver)s" %env):
            with prefix("export WORKON_HOME=%(envserver)s" %env):
                with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                    run('rm -rf %(project)s; rmvirtualenv %(project)s' %env)