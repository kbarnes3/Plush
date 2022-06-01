from colorama import init, Fore
from fabric import Task
from fabric.connection import Connection
from fabric.transfer import Transfer
from patchwork.files import exists as patchwork_exists

import plush.fabric_commands
from plush.fabric_commands import install_packages, prepare_user
from plush.fabric_commands.git import clone
from plush.fabric_commands.permissions import ensure_directory
from plush.fabric_commands.ssh_key import create_key
from plush.repo_keys import add_repo_key


init(autoreset=True)


def exists(conn: Connection, path: str) -> bool:
    # pylint doesn't understand the @set_runner decorator
    # create a wrapper so we only have to suppress the error once
    return patchwork_exists(conn, path) # pylint: disable=E1120


@Task
def setup_user(conn, user, disable_sudo_passwd=False, set_public_key_file=None):
    print(Fore.GREEN + f'Configuring {user}')
    messages = prepare_user(
        conn,
        user,
        'webadmin',
        add_sudo=True,
        no_sudo_passwd=disable_sudo_passwd)
    add_authorized_key(conn, user, set_public_key_file)


    if messages:
        print("========================================")
        print(messages)
        print("========================================")
    print(Fore.GREEN + f'{user} configured')


@Task
def add_authorized_key(conn, user, set_public_key_file):
    if set_public_key_file:
        with open(set_public_key_file, 'r', encoding='utf-8') as public_key:
            public_key_contents = public_key.read()
        plush.fabric_commands.add_authorized_key(conn, user, public_key_contents)

@Task
def disable_ssh_passwords(conn):
    sshd_config = '/etc/ssh/sshd_config'
    conn.sudo(f"sed -i '/^ *PasswordAuthentication/d' {sshd_config}")
    conn.sudo(f'echo "PasswordAuthentication no" | sudo tee -a {sshd_config}', pty=True)
    print("========================================")
    print("Password authentication disabled for SSH.")
    print("Restart the SSH daemon by logging into the console and running:")
    print("sudo service ssh restart")
    print("Alternatively, reboot the server if console access isn't readily available.")
    print("========================================")


@Task
def test_deploy(conn, repo):
    print(Fore.GREEN + 'Starting test deployment')
    owning_group = 'webadmin'
    create_key(conn, repo, owning_group)
    add_repo_key(conn, repo)
    ensure_directory(conn, '/var/src', owning_group)
    if exists(conn, '/var/src/test'):
        conn.sudo('rm -rf /var/src/test')
    clone(conn, repo, '/var/src/test', skip_strict_key_checking=True)
    print(Fore.GREEN + 'Test deployment complete to /var/src/test')


@Task
def compile_requirements(conn, fresh=False, upgrade=False):
    print(Fore.GREEN + 'Compiling Python requirements')
    install_packages(conn, ['python3-venv'])
    remote_user = conn.run('whoami').stdout.strip()

    staging_dir = '/tmp/pip-tools'
    staging_python_dir = f'{staging_dir}/python'

    ensure_directory(conn, staging_dir, remote_user)
    conn.sudo(f'rm -rf {staging_dir}/*')
    ensure_directory(conn, f'{staging_python_dir}', remote_user)
    ensure_directory(conn, f'{staging_python_dir}/plush', remote_user)
    ensure_directory(conn, f'{staging_python_dir}/plush/fabric_commands', remote_user)

    requirements_in = 'test-requirements.in'
    setup_py = 'setup.py'
    readme_rst = 'README.rst'
    requirements_txt = 'ubuntu64-py310-requirements.txt'

    transfer = Transfer(conn)
    transfer.put(requirements_in, f'{staging_dir}/{requirements_in}')
    transfer.put(f'python/{setup_py}', f'{staging_python_dir}/{setup_py}')
    transfer.put(f'python/{readme_rst}', f'{staging_python_dir}/{readme_rst}')

    if not fresh:
        transfer.put(requirements_txt, f'{staging_dir}/{requirements_txt}')

    print(Fore.GREEN + 'Setting up virtualenv')
    with conn.cd(staging_dir):
        conn.run('python3 -m venv venv')

        print(Fore.GREEN + 'Updating pip')
        conn.run('venv/bin/python -m pip install --upgrade pip')

        print(Fore.GREEN + 'Updating pip-tools')
        conn.run('venv/bin/python -m pip install --upgrade pip-tools')

        print(Fore.GREEN + 'Compiling requirements')
        upgrade_flag = ''
        if upgrade:
            upgrade_flag = '--upgrade'
        conn.run(f'venv/bin/pip-compile {upgrade_flag} --output-file={requirements_txt} ' +
                 f'{requirements_in}')

        # Substitute an absolute path to Plush with a relative one
        conn.run("sed -i 's/file:\\/\\/\\/tmp\\/pip-tools\\/python/\\.\\/python/g' " +
                f"{requirements_txt}")


    transfer.get(f'{staging_dir}/{requirements_txt}', requirements_txt)
    print(Fore.GREEN + f'Updated {requirements_txt}')
    print(Fore.GREEN + 'Removing temp files')
    conn.sudo('rm -rf /tmp/pip-tools')
