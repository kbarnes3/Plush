from fabric.connection import Connection
from invoke import UnexpectedExit
from patchwork.files import exists

from .ssh_key import get_keyfile


def prepare_user(conn: Connection, user: str, group: str, add_sudo=True, no_sudo_passwd=False):
    messages = ''
    user_exists = False

    try:
        conn.sudo('getent passwd {0}'.format(user))
        user_exists = True
    except UnexpectedExit:
        pass

    if not user_exists:
        conn.sudo('adduser --disabled-password {0}'.format(user))

    group_exists = False
    try:
        conn.sudo('getent group {0}'.format(group))
        group_exists = True
    except UnexpectedExit:
        pass

    if not group_exists:
        conn.sudo('addgroup {0}'.format(group))

    conn.sudo('adduser {0} {1}'.format(user, group))

    if add_sudo:
        conn.sudo('adduser {0} sudo'.format(user))

    if no_sudo_passwd:
        sudoers_file = '/etc/sudoers.d/{0}-plush'.format(user)
        if exists(conn, sudoers_file, True):
            conn.sudo('rm {0}'.format(sudoers_file))
        conn.sudo("echo '{0} ALL=(ALL:ALL) NOPASSWD:ALL' | sudo EDITOR='tee -a' visudo -f {1}"
                  .format(user, sudoers_file))

    if add_sudo and not no_sudo_passwd:
        messages += 'Ensure {0} has a secure password configured ' \
                    'in order to run commands as sudo.\n'.format(user)
        messages += 'Alternatively, rerun this command with ' \
                    'the no_sudo_passwd=True parameter\n'
    if not user_exists:
        messages += 'The {0} account was created without a password set. ' \
                    'A superuser will need to manually run ' \
                    '\"sudo passwd {0}\"\n'.format(user)
        messages += 'Where possible, consider not setting a password and ' \
                    'instead using key based authentication.\n'

    if messages:
        # Every message line ends in a newline.
        # If we've got a non-empty message, strip the last character
        messages = messages[:-1]

    return messages


def add_authorized_key(conn: Connection, user, public_key):
    conn.sudo('mkdir -p /home/{0}/.ssh'.format(user), user=user)
    conn.sudo('touch /home/{0}/.ssh/authorized_keys'.format(user), user=user)
    conn.sudo('chmod -R go= /home/{0}/.ssh'.format(user), user=user)
    conn.sudo('echo "{0}" | tee -a /home/{1}/.ssh/authorized_keys'
              .format(public_key, user), user=user)
