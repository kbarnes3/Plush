from fabric.connection import Connection
from invoke.watchers import Responder
from patchwork.files import directory, exists


DEFAULT_KEY_DIRECTORY = '/var/deploykeys'


def get_keyfile(project_name, directory=DEFAULT_KEY_DIRECTORY, public=True):
    sanitized_name = project_name.replace('/', '_')
    suffix = '.pub' if public else ''
    keyfile = '{0}/{1}{2}'.format(directory, sanitized_name, suffix)
    return keyfile


def create_key(conn: Connection, project_name, owning_group, path=DEFAULT_KEY_DIRECTORY):
    directory(conn, path, group=owning_group, mode='600', sudo=True)
    keyfile = get_keyfile(project_name, path, public=False)
    if exists(conn, keyfile, sudo=True):
        conn.sudo('rm {0}'.format(keyfile))
    # Automatically provide an empty passphrase
    responder = Responder(r'passphrase.*:', '\n')
    conn.sudo('ssh-keygen -t rsa -b 4096 -C "{0}" -f {1}'.format(project_name, keyfile),
              watchers=[responder])
