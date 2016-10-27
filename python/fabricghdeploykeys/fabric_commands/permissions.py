from fabric.api import cd, sudo


def set_permissions(directory, group, mod, setgid=False):
    with cd(directory):
        sudo('chgrp -R webadmin .'.format(group))
        sudo('chmod -R {0} .'.format(mod))
        sudo('chmod -R ug+X .')

        if setgid:
            sudo('chmod -R g+s .')
