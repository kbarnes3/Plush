Plush
==============

[![Build Status](https://kbarnes3.visualstudio.com/Plush/_apis/build/status/kbarnes3.Plush?branchName=master)](https://kbarnes3.visualstudio.com/Plush/_build/latest?definitionId=8&branchName=master)

A helper library for Fabric to simplify creating and managing GitHub deploy keys when deploying your GitHub-hosted
repository. Currently, Plush is only tested on Ubuntu 18.04 LTS.

Plush aims to make deployments easier by:
- Using OAuth flows to securely connect to the GitHub API on your behalf
(while supporting 2 factor auth and never handling your username/password)
- Generating SSH deploy keys on your target server/computer
- Registering these deploy keys with your GitHub repo programmatically
- Configuring your new clone to use the appropriate deploy key while not conflicting with other 
SSH keys used elsewhere on your server
- ACL'ing these keys so they can be reused by people to fetch/deploy on your behalf
(and not readable by anyone else on the server)
- Example PowerShell scripts are provided that give tab completion around fab.exe

To see this project in action, follow the directions in Setup-Dev-Environment.md. You will need access to an Ubuntu 18.04 machine (ideally a VM).

To get started, see fabfile.py for a minimal usage of Plush. For a more complete example, see my [BaseDjangoSite template](https://github.com/kbarnes3/BaseDjangoSite).

