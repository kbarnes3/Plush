from plush.fabric_commands import setup_user
from plush.repo_keys import add_repo_key
from plush.fabric_commands.git import clone
from plush.fabric_commands.permissions import make_directory
from plush.fabric_commands.ssh_key import create_key


def test_deploy():
    repo_full_name = 'kbarnes3/Plush'
    owning_group = 'webadmin'
    create_key(repo_full_name, owning_group)
    add_repo_key(repo_full_name)
    make_directory(owning_group, '/var/src')
    clone(repo_full_name, '/var/src/test')
