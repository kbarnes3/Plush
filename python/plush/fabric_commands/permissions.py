from typing import Optional
from fabric.connection import Connection


def ensure_directory(conn: Connection,
                     directory: str,
                     owning_group: str,
                     mod: str = 'ug+rwX,o+rX,o-w'):
    conn.sudo('mkdir -p {0}'.format(directory))
    set_permissions_directory(conn, directory, group=owning_group, mod=mod)


def set_permissions_directory(conn: Connection,
                              directory: str,
                              group: Optional[str] = None,
                              user: Optional[str] = None,
                              mod: str = '660',
                              setgid: bool = True):
    if group is not None:
        conn.sudo('chgrp -R {0} {1}'.format(group, directory))

    if user is not None:
        conn.sudo('chown -R {0} {1}'.format(user, directory))

    conn.sudo('chmod -R {0} {1}'.format(mod, directory))

    if setgid:
        conn.sudo('chmod -R g+s {0}'.format(directory))


def set_permissions_file(conn: Connection,
                         file: str,
                         user: Optional[str] = None,
                         group: Optional[str] = None,
                         mod: str = '644'):
    if group is not None:
        conn.sudo('chgrp {0} {1}'.format(group, file))

    if user is not None:
        conn.sudo('chown {0} {1}'.format(user, file))

    conn.sudo('chmod {0} {1}'.format(mod, file))
