import os
from github import Github, GithubException
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.contrib import keyring_storage
from oauth2client.tools import run_flow


CLIENT_ID = '1fe774845dda5a15936d'
CLIENT_SECRET = '5212960321bcd875538f2221769ae74612e27a04'
SCOPE = 'repo'
AUTH_URI = 'https://github.com/login/oauth/authorize'
TOKEN_URI = 'https://github.com/login/oauth/access_token'


class AuthException(Exception):
    def __init__(self, message):
        self.message = message


def run_oauth_flow():
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, SCOPE, auth_uri=AUTH_URI, token_uri=TOKEN_URI)
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
        return False

    user = api.get_user()

    try:
        print("Successfully authenticated as {0} (Name: '{1}' Email: '{2}')".format(user.login, user.name, user.email))
        return True
    except GithubException as exception:
        print('Failed with {0}, data: {1}'.format(exception.status, exception.data))
        print('Unable to verify local auth token. Run \'auth\' to reset')

    return False


def delete_access_token():
    storage = _get_storage()
    storage.delete()


def _get_storage():
    return keyring_storage.Storage('PlushKeys', 'default')
