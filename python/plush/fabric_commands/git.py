from fabric.connection import Connection
from ..fabric_commands import install_packages
from .ssh_key import get_keyfile


def clone(conn: Connection, repo_full_name: str, path: str, skip_strict_key_checking=False):
    install_packages(conn, ['git'])
    keyfile = get_keyfile(repo_full_name, public=False)
    conn.sudo('git config --system protocol.ext.allow always')
    strict_key_checking = '-o StrictHostKeyChecking=no ' if skip_strict_key_checking else ''
    conn.sudo("git clone 'ext::ssh -i {0} {1}git@github.com %S {2}.git' {3}".format(
        keyfile,
        strict_key_checking,
        repo_full_name,
        path))
