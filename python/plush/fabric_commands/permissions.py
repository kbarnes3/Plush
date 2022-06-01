from typing import Optional
from fabric.connection import Connection
from patchwork.files import exists as patchwork_exists


def _exists(conn: Connection, path: str, sudo: bool=False) -> bool:
    # pylint doesn't understand the @set_runner decorator
    # create a wrapper so we only have to suppress the error once
    return patchwork_exists(conn, path, sudo=sudo) # pylint: disable=E1120


def ensure_directory(conn: Connection,
                     directory: str,
                     owning_group: str,
                     mod: str = 'ug+rwX,o+rX,o-w'):
    conn.sudo(f'mkdir -p {directory}')
    set_permissions_directory(conn, directory, group=owning_group, mod=mod)


def set_permissions_directory(conn: Connection, # pylint: disable=R0913
                              directory: str,
                              group: Optional[str] = None,
                              user: Optional[str] = None,
                              mod: str = '660',
                              setgid: bool = True):
    if group is not None:
        conn.sudo(f'chgrp -R {group} {directory}')

    if user is not None:
        conn.sudo(f'chown -R {user} {directory}')

    conn.sudo(f'chmod -R {mod} {directory}')

    if setgid:
        conn.sudo(f'chmod -R g+s {directory}')


def set_permissions_file(conn: Connection,
                         file: str,
                         user: Optional[str] = None,
                         group: Optional[str] = None,
                         mod: str = '644'):
    if group is not None:
        conn.sudo(f'chgrp {group} {file}')

    if user is not None:
        conn.sudo(f'chown {user} {file}')

    conn.sudo(f'chmod {mod} {file}')
