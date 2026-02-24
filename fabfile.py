from colorama import init, Fore
from fabric import Task
from fabric.connection import Connection
from plush.patchwork.files import exists as patchwork_exists

import plush.fabric_commands
from plush.fabric_commands import prepare_user
from plush.fabric_commands.git import clone
from plush.fabric_commands.permissions import ensure_directory
from plush.fabric_commands.ssh_key import create_key
from plush.repo_keys import add_repo_key


init(autoreset=True)


def exists(conn: Connection, path: str) -> bool:
    # pylint doesn't understand the @set_runner decorator
    # create a wrapper so we only have to suppress the error once
    return patchwork_exists(conn, path) # pylint: disable=E1120


@Task
def setup_user(conn, user, disable_sudo_passwd=False, set_public_key_file=None):
    print(Fore.GREEN + f'Configuring {user}')
    messages = prepare_user(
        conn,
        user,
        'webadmin',
        add_sudo=True,
        no_sudo_passwd=disable_sudo_passwd)
    add_authorized_key(conn, user, set_public_key_file)


    if messages:
        print("========================================")
        print(messages)
        print("========================================")
    print(Fore.GREEN + f'{user} configured')


@Task
def add_authorized_key(conn, user, set_public_key_file):
    if set_public_key_file:
        with open(set_public_key_file, 'r', encoding='utf-8') as public_key:
            public_key_contents = public_key.read()
        plush.fabric_commands.add_authorized_key(conn, user, public_key_contents)

@Task
def disable_ssh_passwords(conn):
    sshd_config = '/etc/ssh/sshd_config'
    sshd_config_dir = '/etc/ssh/sshd_config.d/'
    conn.sudo(f"sed -i '/^ *PasswordAuthentication/d' {sshd_config}")
    conn.sudo(f"find {sshd_config_dir} -type f -execdir " +
              "sed -i '/^ *PasswordAuthentication/d' {} \\;")
    conn.sudo(f'echo "PasswordAuthentication no" | sudo tee -a {sshd_config}', pty=True)
    print("========================================")
    print("Password authentication disabled for SSH.")
    print("Restart the SSH daemon by logging into the console and running:")
    print("sudo service ssh restart")
    print("Alternatively, reboot the server if console access isn't readily available.")
    print("========================================")

@Task
def test_deploy(conn, repo):
    print(Fore.GREEN + 'Starting test deployment')
    owning_group = 'webadmin'
    create_key(conn, repo, owning_group)
    add_repo_key(conn, repo)
    ensure_directory(conn, '/var/src', owning_group)
    if exists(conn, '/var/src/test'):
        conn.sudo('rm -rf /var/src/test')
    clone(conn, repo, '/var/src/test', skip_strict_key_checking=True)
    print(Fore.GREEN + 'Test deployment complete to /var/src/test')
