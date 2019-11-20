from typing import Optional
from fabric.connection import Connection


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
