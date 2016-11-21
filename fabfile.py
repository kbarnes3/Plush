from fabricghdeploykeys.fabric_commands import setup_user
from fabricghdeploykeys.fabric_commands.git import clone
from fabricghdeploykeys.fabric_commands.permissions import make_directory
from fabricghdeploykeys.fabric_commands.ssh_key import create_key


def test_deploy():
    repo_full_name = 'kbarnes3/FabricGHDeployKeys'
    owning_group = 'webadmin'
    create_key(repo_full_name, owning_group)
    make_directory(owning_group, '/var/src')
    clone(repo_full_name, '/var/src/test')
