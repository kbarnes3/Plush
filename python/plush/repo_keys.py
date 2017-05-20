from fabric.api import run, sudo
from github import GithubException
from .oauth_flow import get_api
from .fabric_commands import get_keyfile


def list_repo_keys(repo_full_name):
    api = get_api()

    repo = api.get_repo(repo_full_name)
    deploy_keys = repo.get_keys()

    try:
        for key in deploy_keys:
            print(key.title)
    except GithubException as exception:
        print('Failed with {0}, data: {1}'.format(exception.status, exception.data))


def add_repo_key(repo_full_name, key_name=''):
    public_keyfile = get_keyfile(repo_full_name)
    public_keyfile_contents = sudo('cat {0}'.format(public_keyfile))

    if key_name == '':
        # Default the key_name to the hostname we are connected to
        key_name = run('hostname')

    api = get_api()

    repo = api.get_repo(repo_full_name)

    try:
        repo.create_key(key_name, public_keyfile_contents, read_only=True)
    except GithubException as exception:
        print('Failed with {0}, data: {1}'.format(exception.status, exception.data))
