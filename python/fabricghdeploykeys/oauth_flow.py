import os
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib import keyring_storage
from oauth2client.tools import run_flow


def run_oauth_flow():
    directory = os.path.dirname(__file__)
    secrets_path = os.path.join(directory, 'client_secrets.json')
    flow = flow_from_clientsecrets(secrets_path, 'repo')
    storage = keyring_storage.Storage('FabricGHDeployKeys', 'default')
    cred = run_flow(flow, storage)

    if cred is not None:
        return cred.access_token
    else:
        return None


def get_access_token():
    storage = keyring_storage.Storage('FabricGHDeployKeys', 'default')
    cred = storage.get()
    return cred.access_token
