from fabricghdeploykeys.fabric_commands import setup_user
from fabricghdeploykeys.fabric_commands.ssh_key import make_key_dir, create_key


def test_deploy():
    project_name = 'FabricGHDeployKeys'
    owning_group = 'webadmin'
    create_key(project_name, owning_group)
