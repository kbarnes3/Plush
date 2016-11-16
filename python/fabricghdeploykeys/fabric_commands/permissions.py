from fabric.api import cd, sudo


def make_directory(owning_group, directory, mod='660'):
    sudo('mkdir -p {0}'.format(directory))
    set_permissions(directory, owning_group, mod)


def set_permissions(directory, group, mod='660', setgid=True):
    with cd(directory):
        sudo('chgrp -R webadmin .'.format(group))
        sudo('chmod -R {0} .'.format(mod))
        sudo('chmod -R ug+X .')

        if setgid:
            sudo('chmod -R g+s .')
