# coding: utf-8
from fabric.api import env, require, run, task
from fabric.context_managers import prefix
import db

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

    with prefix("export PROJECT_HOME=$HOME/www"):
        with prefix("export WORKON_HOME=$HOME/env"):
            with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                run("mkproject %(project)s" % env)


@task
def requirements():
    """
    :: Update Python dependencies on remote host.
    """
    require('project', provided_by=('staging', 'production'))

    with prefix("export PROJECT_HOME=$HOME/www"):
        with prefix("export WORKON_HOME=$HOME/env"):
            with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                run("workon %(project)s; pip install -r %(requirements)s; deactivate" % env)


@task
def init():
    """
    :: Initialize remote host environment.
    """
    require('root', provided_by=('staging', 'production'))

    # Create virtualenv to wrap the environment
    virtualenv()
    # Send the project to the remote host
    deploy.send()
    # Install dependencies on the virtualenv
    requirements()
    # Create the database
    db.syncdb()