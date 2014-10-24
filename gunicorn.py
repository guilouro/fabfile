#coding: utf-8
from fabric.api import run, require, prefix, env, task

@task
def start():
    """
    :: Started gunicorn on server
    """
    require('project', provided_by=('staging', 'production'))
    with prefix("export PROJECT_HOME=%(projserver)s" %env):
        with prefix("export WORKON_HOME=%(envserver)s" %env):
            with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                run("workon %(project)s; gunicorn -w3 %(gunicorn_wsgi_app)s --bind %(gunicorn_bind)s --pid %(gunicorn_pidfile)s -D; deactivate" %env)

@task
def stop():
	"""
	:: Stoped gunicorn on server
	"""
	require('gunicorn_pidfile', provided_by=('staging', 'production'))

	run('kill `cat %(gunicorn_pidfile)s`' %env)


@task
def reload():
	"""
    :: Reloaded gunicorn on server
    """
	stop()
	start()