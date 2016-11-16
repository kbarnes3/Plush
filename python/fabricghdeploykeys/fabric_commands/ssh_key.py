from fabric.api import run, sudo

from .permissions import make_directory, set_permissions


DEFAULT_KEY_DIRECTORY = '/var/deploykeys'


def get_keyfile(project_name, directory=DEFAULT_KEY_DIRECTORY):
    keyfile = '{0}/{1}'.format(directory, project_name)
    return keyfile


def create_key(project_name, owning_group, directory=DEFAULT_KEY_DIRECTORY):
    make_directory(owning_group, directory, mod='600')
    keyfile = get_keyfile(project_name, directory)
    sudo('ssh-keygen -t rsa -b 4096 -C "{0}" -f {1}'.format(project_name, keyfile))
    set_permissions(directory, owning_group, mod='600')
