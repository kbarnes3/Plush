from fabric.api import sudo
from .ssh_key import get_keyfile


def clone(repo_full_name, path, skip_strict_key_checking=False):
    keyfile = get_keyfile(repo_full_name, public=False)
    strict_key_checking = '-o StrictHostKeyChecking=no ' if skip_strict_key_checking else ''
    sudo("git clone 'ext::ssh -i {0} {1}git@github.com %S {2}.git' {3}".format(
        keyfile,
        strict_key_checking,
        repo_full_name,
        path))
