from fabric.api import sudo

from .permissions import set_permissions


def make_key_dir(owning_group, directory='/var/deploykeys'):
    sudo('mkdir -p {0}'.format(directory))
    set_permissions(directory, owning_group, '660', setgid=True)
