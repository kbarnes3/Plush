from fabric.api import sudo
from .ssh_key import get_keyfile


def clone(project_name, project_owner, path):
    keyfile = get_keyfile(project_name)
    sudo("git clone 'ext::ssh -i {0} git@github.com %S {1}/{2}.git' {3}".format(keyfile, project_owner, project_name, path))
