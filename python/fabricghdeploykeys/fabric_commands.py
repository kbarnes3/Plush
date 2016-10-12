from fabric.api import settings, sudo


class _AllowedException(Exception):
    pass


def setup_user(user, group):
    user_exists = False

    with settings(abort_exception=_AllowedException):
        try:
            sudo('getent passwd {0}'.format(user))
            user_exists = True
        except _AllowedException:
            pass

    if user_exists:
        sudo('echo Yep')
    else:
        sudo('echo Nope')


def create_deploy_key(repo_full_name):
    pass
