from typing import Iterable

from fabric.connection import Connection
from invoke import UnexpectedExit
from invoke.watchers import Responder
from patchwork.files import exists

from .ssh_key import get_keyfile


__all__ = ['prepare_user', 'add_authorized_key', 'install_packages', 'get_keyfile']


def prepare_user(conn: Connection, user: str, group: str, add_sudo=True, no_sudo_passwd=False):
    messages = ''
    user_exists = False

    try:
        conn.sudo('getent passwd {0}'.format(user))
        user_exists = True
    except UnexpectedExit:
        pass

    if not user_exists:
        # Handle all the prompts for information about the new user like their name and room number
        responder = Responder(r'.*\[.*\].*', '\n')
        conn.sudo('adduser --disabled-password {0}'.format(user), pty=True, watchers=[responder])

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
        if exists(conn, sudoers_file, sudo=True):
            conn.sudo('rm {0}'.format(sudoers_file))
        conn.sudo("echo '{0} ALL=(ALL:ALL) NOPASSWD:ALL' | sudo EDITOR='tee -a' visudo -f {1}"
                  .format(user, sudoers_file), pty=True)

    if add_sudo and not no_sudo_passwd:
        messages += 'Ensure {0} has a secure password configured ' \
                    'in order to run commands as sudo.\n'.format(user)
        messages += 'Alternatively, rerun this command with ' \
                    'the no_sudo_passwd=True parameter\n'
    if not user_exists:
        messages += 'The {0} account was created without a password set. ' \
                    'If a password is needed, a superuser will need to manually run: \n' \
                    'sudo passwd {0}\n' \
                    'Where possible, consider not setting a password and ' \
                    'instead using key based authentication.\n'.format(user)

    if messages:
        # Every message line ends in a newline.
        # If we've got a non-empty message, strip the last character
        messages = messages[:-1]

    return messages


def add_authorized_key(conn: Connection, user, public_key):
    conn.sudo('mkdir -p /home/{0}/.ssh'.format(user), user=user)
    conn.sudo('touch /home/{0}/.ssh/authorized_keys'.format(user), user=user)
    conn.sudo('chmod -R go= /home/{0}/.ssh'.format(user), user=user)
    conn.sudo('echo "{0}" | sudo tee -a /home/{1}/.ssh/authorized_keys'
              .format(public_key, user), pty=True)


def install_packages(conn: Connection, packages: Iterable[str]):
    apt = "DEBIAN_FRONTEND=noninteractive apt-get install -y {}"
    for package in packages:
        conn.sudo(apt.format(package))
