import os
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib import keyring_storage
from oauth2client.tools import run_flow


def run_oauth_flow():
    dir = os.path.dirname(__file__)
    secrets_path = os.path.join(dir, 'client_secrets.json')
    flow = flow_from_clientsecrets(secrets_path, '')
    storage = keyring_storage.Storage('FabricGHDeployKeys', 'default')
    run_flow(flow, storage)
