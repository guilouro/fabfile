# coding: utf-8
from fabric.api import env, require, run, task
from fabric.context_managers import prefix
from fabric.contrib.project import rsync_project


@task
def send():
    """
    :: Send the code to the remote host.
    """
    require('project_server_path', provided_by=('staging', 'production'))

    # Copy the project
    rsync_project(
        remote_dir=env.project_server_path,
        local_dir=env.project_local_path + "/",
        exclude=[
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
            'src',
        ],
        delete=True,
        extra_opts='--omit-dir-times',
    )


@task
def collectstatic():
    """
    :: Collect all static files from Django apps and copy them into the public static folder.
    """
    require('project_server_path', provided_by=('staging', 'production'))

    run(('source %(activate)s; python %(manage)s collectstatic; deactivate') % env)