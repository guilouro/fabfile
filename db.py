# coding: utf-8
from fabric.api import env, require, run, task
from fabric.context_managers import prefix


@task
def syncdb():
    """
    :: Execute syncdb on remote host.
    """
    require('virtualenv_activate', provided_by=('staging', 'production'))

    run(('source %(virtualenv_activate)s; python %(manage_file)s syncdb') % env)