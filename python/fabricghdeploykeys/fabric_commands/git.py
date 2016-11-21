from fabric.api import sudo
from .ssh_key import get_keyfile


def clone(repo_full_name, path):
    keyfile = get_keyfile(repo_full_name, public=False)
    sudo("git clone 'ext::ssh -i {0} git@github.com %S {1}.git' {2}".format(keyfile, repo_full_name, path))
