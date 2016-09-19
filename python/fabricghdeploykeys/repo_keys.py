from github import Github, GithubException
from .oauth_flow import get_access_token


def list_repo_keys(repo_full_name):
    token = get_access_token()
    api = Github(token)

    repo = api.get_repo(repo_full_name)
    deploy_keys = repo.get_keys()

    try:
        for key in deploy_keys:
            print(key.title)
    except GithubException as exception:
        print('Failed with {0}, data: {1}'.format(exception.status, exception.data))
