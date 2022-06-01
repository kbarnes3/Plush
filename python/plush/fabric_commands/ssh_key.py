from fabric.connection import Connection
from invoke.watchers import Responder

from .permissions import _exists, ensure_directory

DEFAULT_KEY_DIRECTORY = '/var/deploykeys'


def get_keyfile(project_name, directory=DEFAULT_KEY_DIRECTORY, public=True):
    sanitized_name = project_name.replace('/', '_')
    suffix = '.pub' if public else ''
    keyfile = f'{directory}/{sanitized_name}{suffix}'
    return keyfile


def create_key(conn: Connection, project_name, owning_group, path=DEFAULT_KEY_DIRECTORY):
    ensure_directory(conn, path, owning_group, mod='600')
    keyfile = get_keyfile(project_name, path, public=False)
    if _exists(conn, keyfile, sudo=True):
        conn.sudo(f'rm {keyfile}')
    # Automatically provide an empty passphrase
    responder = Responder(r'passphrase.*:', '\n')
    conn.sudo(f'ssh-keygen -t rsa -b 4096 -C "{project_name}" -f {keyfile}',
              watchers=[responder])
