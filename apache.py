#coding: utf-8
from fabric.api import run, task, require, env
from fabric.operations import put

@task
def upload_apache_conf():
    """
    :: Upload the apache.conf
    """
    require('project', provided_by=('staging', 'production', ))

    env.apache_conf = '%(project_local_path)s/%(project)s/%(project)s.conf' % env
    env.apache_path = '/home/%(user)s/.apache-conf/' % env

    put('%(apache_conf)s' % env, '%(apache_path)s' % env)

    run('ls -la %(apache_path)s' % env)


@task
def remove_conf():
    """
    :: Remove the apache.conf
    """
    require('project', provided_by=('staging', 'production', ))

    env.apache_file = '/home/%(user)s/.apache-conf/%(project)s.conf' % env

    run('rm %(apache_file)s' % env)