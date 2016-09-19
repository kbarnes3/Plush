import os
from github import Github, GithubException
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib import keyring_storage
from oauth2client.tools import run_flow


class AuthException(Exception):
    def __init__(self, message):
        self.message = message


def run_oauth_flow():
    directory = os.path.dirname(__file__)
    secrets_path = os.path.join(directory, 'client_secrets.json')
    flow = flow_from_clientsecrets(secrets_path, 'repo')
    storage = _get_storage()
    cred = run_flow(flow, storage)

    verify_access_token()

    if cred is not None:
        return cred.access_token
    else:
        return None


def get_api():
    storage = _get_storage()
    cred = storage.get()
    if cred is None:
        raise AuthException('No local authorization found. Run \'auth\' to add one')

    token = cred.access_token
    api = Github(token)
    return api


def verify_access_token():
    try:
        api = get_api()
    except AuthException as exception:
        print('Error: {0}'.format(exception.message))
        return

    user = api.get_user()

    try:
        print("Successfully authenticated as {0} (Name: '{1}' Email: '{2}')".format(user.login, user.name, user.email))
    except GithubException as exception:
        print('Failed with {0}, data: {1}'.format(exception.status, exception.data))
        print('Unable to verify local auth token. Run \'auth\' to reset')


def delete_access_token():
    storage = _get_storage()
    storage.delete()


def _get_storage():
    return keyring_storage.Storage('FabricGHDeployKeys', 'default')
