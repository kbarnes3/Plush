from fabric.api import cd, sudo


def make_directory(owning_group, directory, mod='ug+rwX,o+rX,o-w'):
    sudo('mkdir -p {0}'.format(directory))
    set_permissions_directory(directory, group=owning_group, mod=mod)


def set_permissions_directory(directory, group=None, user=None, mod='660', setgid=True):
    with cd(directory):
        if group is not None:
            sudo('chgrp -R {0} .'.format(group))

        if user is not None:
            sudo('chown -R {0} .'.format(user))

        sudo('chmod -R {0} .'.format(mod))

        if setgid:
            sudo('chmod -R g+s .')


def set_permissions_file(file, user=None, group=None, mod='644'):
    if group is not None:
        sudo('chgrp {0} {1}'.format(group, file))

    if user is not None:
        sudo('chown {0} {1}'.format(user, file))

    sudo('chmod {0} {1}'.format(mod, file))
