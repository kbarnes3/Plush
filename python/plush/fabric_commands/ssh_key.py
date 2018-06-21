from fabric.api import run, sudo
from fabric.contrib.files import exists

from .permissions import make_directory, set_permissions_directory


DEFAULT_KEY_DIRECTORY = '/var/deploykeys'


def get_keyfile(project_name, directory=DEFAULT_KEY_DIRECTORY, public=True):
    sanitized_name = project_name.replace('/', '_')
    suffix = '.pub' if public else ''
    keyfile = '{0}/{1}{2}'.format(directory, sanitized_name, suffix)
    return keyfile


def create_key(project_name, owning_group, directory=DEFAULT_KEY_DIRECTORY):
    make_directory(owning_group, directory, mod='600')
    keyfile = get_keyfile(project_name, directory, public=False)
    if exists(keyfile, use_sudo=True):
        sudo('rm {0}'.format(keyfile))
    sudo('ssh-keygen -t rsa -b 4096 -C "{0}" -f {1}'.format(project_name, keyfile))
    set_permissions_directory(directory, owning_group, mod='600')
