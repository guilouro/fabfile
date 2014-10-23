# coding: utf-8
from fabric.api import env, require, run, task
from fabric.context_managers import prefix


@task
def send():
    """
    :: Send the code to the remote host.
    """
    require('server_path', provided_by=('staging', 'production'))

    # Copy the project
    rsync_project(
        remote_dir=env.server_path,
        local_dir=env.local_path + "/",
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts='--omit-dir-times',
    )


@task
def collectstatic():
    """
    :: Collect all static files from Django apps and copy them into the public static folder.
    """
    require('server_path', provided_by=('staging', 'production'))
    run(('source %(virtualenv_activate)s; '
            'python %(manage_file)s collectstatic; '
            'deactivate') % env,
    )