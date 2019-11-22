import os
from fabric import task
from patchwork.files import directory, exists


@task
def setup_user(conn, user, public_key_file=None, no_sudo_passwd=False):
    from plush.fabric_commands import prepare_user

    messages = prepare_user(conn, user, 'webadmin', add_sudo=True, no_sudo_passwd=no_sudo_passwd)
    add_authorized_key(conn, user, public_key_file)
    if messages:
        print("========================================")
        print(messages)
        print("========================================")


@task
def add_authorized_key(conn, user, public_key_file):
    import plush.fabric_commands
    if public_key_file:
        with open(public_key_file, 'r') as public_key:
            public_key_contents = public_key.read()
        plush.fabric_commands.add_authorized_key(conn, user, public_key_contents)


@task
def test_deploy(conn, repo):
    from plush.repo_keys import add_repo_key
    from plush.fabric_commands.git import clone
    from plush.fabric_commands.ssh_key import create_key

    owning_group = 'webadmin'
    create_key(conn, repo, owning_group)
    add_repo_key(conn, repo)
    directory(conn, '/var/src', group=owning_group, sudo=True)
    if exists(conn, '/var/src/test'):
        conn.sudo('rm -rf /var/src/test')
    clone(conn, repo, '/var/src/test', skip_strict_key_checking=True)
