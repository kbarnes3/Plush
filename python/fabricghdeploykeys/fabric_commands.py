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

    if not user_exists:
        sudo('adduser {0}'.format(user))

    group_exists = False
    with settings(abort_exception=_AllowedException):
        try:
            sudo('getent group {0}'.format(group))
            group_exists = True
        except _AllowedException:
            pass

    if not group_exists:
        sudo('addgroup {0}'.format(group))

    sudo('adduser {0} sudo'.format(user))
    sudo('adduser {0} {1}'.format(user, group))


def create_deploy_key(repo_full_name):
    pass
