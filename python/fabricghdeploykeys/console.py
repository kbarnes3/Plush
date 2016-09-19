from argparse import ArgumentParser
from sys import argv
from .oauth_flow import run_oauth_flow
from .repo_keys import list_repo_keys


def auth_entry():
    parser = ArgumentParser(prog='auth', description='Manages authorization to GitHub')
    auth_choice = 'auth'
    verify_choice = 'verify'
    delete_choice = 'delete'
    parser.add_argument('action', choices=[auth_choice, verify_choice, delete_choice],
                        help='Get authorization, verify existing authorization, or remove your local authorization',
                        nargs='?',
                        default=auth_choice)
    args = parser.parse_args(argv[1:])

    actions = {
        auth_choice: run_oauth_flow,
        verify_choice: lambda: None,
        delete_choice: lambda: None,
    }

    command = actions[args.action]
    command()


def list_keys_entry():
    parser = ArgumentParser(prog='listkeys', description='Lists the deploy keys for the given repro')
    parser.add_argument('repo_name', help='The full name of the repo (e.g., octocat/Hello-World)')
    args = parser.parse_args(argv[1:])
    list_repo_keys(args.repo_name)
