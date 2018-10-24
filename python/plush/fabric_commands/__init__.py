from fabric.api import settings, sudo
from fabric.contrib.files import exists
from .ssh_key import get_keyfile


class _AllowedException(Exception):
    pass


def prepare_user(user, group, add_sudo=True, no_sudo_passwd=False):
    messages = ''
    user_exists = False

    with settings(abort_exception=_AllowedException):
        try:
            sudo('getent passwd {0}'.format(user))
            user_exists = True
        except _AllowedException:
            pass

    if not user_exists:
        sudo('adduser --disabled-password {0}'.format(user))

    group_exists = False
    with settings(abort_exception=_AllowedException):
        try:
            sudo('getent group {0}'.format(group))
            group_exists = True
        except _AllowedException:
            pass

    if not group_exists:
        sudo('addgroup {0}'.format(group))

    sudo('adduser {0} {1}'.format(user, group))

    if add_sudo:
        sudo('adduser {0} sudo'.format(user))

    if no_sudo_passwd:
        sudoers_file = '/etc/sudoers.d/{0}-plush'.format(user)
        if exists(sudoers_file, True):
            sudo('rm {0}'.format(sudoers_file))
        sudo("echo '{0} ALL=(ALL:ALL) NOPASSWD:ALL' | sudo EDITOR='tee -a' visudo -f {1}".format(user, sudoers_file))

    if add_sudo and not no_sudo_passwd:
        messages += 'Ensure {0} has a secure password configured in order to run commands as sudo.\n'.format(user)
    if not user_exists:
        messages += 'The {0} account was created without a password set. A superuser will need to manually run ' \
                    '\"sudo passwd {0}\"'.format(user)

