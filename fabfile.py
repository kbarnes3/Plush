from fabricghdeploykeys.fabric_commands import setup_user
from fabricghdeploykeys.fabric_commands.git import clone
from fabricghdeploykeys.fabric_commands.permissions import make_directory
from fabricghdeploykeys.fabric_commands.ssh_key import create_key


def test_deploy():
    project_name = 'FabricGHDeployKeys'
    project_owner = 'kbarnes3'
    owning_group = 'webadmin'
    #create_key(project_name, owning_group)
    make_directory(owning_group, '/var/src')
    clone(project_name, project_owner, '/var/src/test')

