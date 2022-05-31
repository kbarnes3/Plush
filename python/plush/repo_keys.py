from typing import Optional

from fabric.connection import Connection
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
        print(f'Failed with {exception.status}, data: {exception.data}')


def add_repo_key(conn: Connection, repo_full_name: str, key_name: Optional[str] = None):
    public_keyfile = get_keyfile(repo_full_name)
    public_keyfile_contents = conn.sudo(f'cat {public_keyfile}').stdout
    public_keyfile_contents = public_keyfile_contents.rstrip()

    if not key_name:
        # Default the key_name to the hostname we are connected to
        key_name = conn.run('hostname').stdout
        key_name = key_name.rstrip()

    api = get_api()

    repo = api.get_repo(repo_full_name)

    try:
        print(f'key_name: "{key_name}"')
        repo.create_key(key_name, public_keyfile_contents, read_only=True)
    except GithubException as exception:
        print(f'Failed with {exception.status}, data: {exception.data}')
        raise exception
