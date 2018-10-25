from fabric.api import env

env.use_ssh_config = True  # This makes it easier to use key based authentication


def setup_user(user, no_sudo_passwd='', public_key_file=''):
    from plush.fabric_commands import prepare_user

    prepare_user(user, 'webadmin', add_sudo=True, no_sudo_passwd=bool(no_sudo_passwd))
    add_authorized_key(user, public_key_file)


def add_authorized_key(user, public_key_file):
    import plush.fabric_commands
    if public_key_file:
        with open(public_key_file, 'r') as public_key:
            public_key_contents = public_key.read()
        plush.fabric_commands.add_authorized_key(user, public_key_contents)


def test_deploy():
    from fabric.api import sudo
    from fabric.contrib.files import exists
    from plush.repo_keys import add_repo_key
    from plush.fabric_commands.git import clone
    from plush.fabric_commands.permissions import make_directory
    from plush.fabric_commands.ssh_key import create_key

    repo_full_name = 'kbarnes3/Plush'
    owning_group = 'webadmin'
    create_key(repo_full_name, owning_group)
    add_repo_key(repo_full_name)
    make_directory(owning_group, '/var/src')
    if exists('/var/src/test'):
        sudo('rm -rf /var/src/test')
    clone(repo_full_name, '/var/src/test', skip_strict_key_checking=True)
