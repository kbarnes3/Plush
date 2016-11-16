from fabric.api import run, sudo

from .permissions import set_permissions


DEFAULT_KEY_DIRECTORY = '/var/deploykeys'


def make_key_dir(owning_group, directory=DEFAULT_KEY_DIRECTORY):
    sudo('mkdir -p {0}'.format(directory))
    _set_key_dir_permissions(directory, owning_group)


def create_key(project_name, owning_group, directory=DEFAULT_KEY_DIRECTORY):
    keyfile = '{0}/{1}'.format(directory, project_name)
    run('ssh-keygen -t rsa -b 4096 -C "{0}" -f {1}'.format(project_name, keyfile))
    _set_key_dir_permissions(directory, owning_group)


def _set_key_dir_permissions(directory, owning_group):
    set_permissions(directory, owning_group, '660', setgid=True)
