from typing import Iterable

from colorama import init, Fore, Style
from colorama.initialise import orig_stdout
from fabric.connection import Connection
from invoke import UnexpectedExit
from invoke.watchers import Responder

from .permissions import _exists
from .ssh_key import get_keyfile


def _ensure_colorama_init():
    if not orig_stdout:
        init()


def prepare_user(conn: Connection, user: str, group: str, add_sudo=True, no_sudo_passwd=False):
    messages = ''
    user_exists = False

    try:
        conn.sudo(f'getent passwd {user}')
        user_exists = True
    except UnexpectedExit:
        pass

    if not user_exists:
        # Handle all the prompts for information about the new user like their name and room number
        responder = Responder(r'.*\[.*\].*', '\n')
        conn.sudo(f'adduser --disabled-password {user}', pty=True, watchers=[responder])

    group_exists = False
    try:
        conn.sudo(f'getent group {group}')
        group_exists = True
    except UnexpectedExit:
        pass

    if not group_exists:
        conn.sudo(f'addgroup {group}')

    conn.sudo(f'adduser {user} {group}')

    if add_sudo:
        conn.sudo(f'adduser {user} sudo')

    if no_sudo_passwd:
        sudoers_file = f'/etc/sudoers.d/{user}-plush'
        if _exists(conn, sudoers_file, sudo=True):
            conn.sudo(f'rm {sudoers_file}')
        conn.sudo(f"echo '{user} ALL=(ALL:ALL) NOPASSWD:ALL' | sudo EDITOR='tee -a' visudo -f " +
                  f"{sudoers_file}", pty=True)

    if add_sudo and not no_sudo_passwd:
        messages += f'Ensure {user} has a secure password configured ' \
                     'in order to run commands as sudo.\n' \
                     'Alternatively, rerun this command with ' \
                     'the no_sudo_passwd=True parameter\n'
    if not user_exists:
        messages += f'The {user} account was created without a password set. ' \
                     'If a password is needed, a superuser will need to manually run: \n' \
                    f'sudo passwd {user}\n' \
                     'Where possible, consider not setting a password and ' \
                     'instead using key based authentication.\n'

    if messages:
        # Every message line ends in a newline.
        # If we've got a non-empty message, strip the last character
        messages = messages[:-1]

    return messages


def add_authorized_key(conn: Connection, user, public_key):
    conn.sudo(f'mkdir -p /home/{user}/.ssh', user=user)
    conn.sudo(f'touch /home/{user}/.ssh/authorized_keys', user=user)
    conn.sudo(f'chmod -R go= /home/{user}/.ssh'.format(user), user=user)
    conn.sudo(f'echo "{public_key}" | sudo tee -a /home/{user}/.ssh/authorized_keys',
              pty=True)


def install_packages(conn: Connection, packages: Iterable[str]):
    _ensure_colorama_init()
    apt = "DEBIAN_FRONTEND=noninteractive apt-get install -y {}"
    for package in packages:
        print(Fore.GREEN + f'Installing {package}' + Style.RESET_ALL)
        conn.sudo(apt.format(package))
