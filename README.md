Plush
==============

A helper library for Fabric to simplify creating and managing GitHub deploy keys when deploying your GitHub-hosted
repository.

Plush aims to make deployments easier by:
- Using OAuth flows to securely connect to the GitHub API on your behalf
(while supporting 2 factor auth and never handling your username/password)
- Generating SSH deploy keys on your target computer
- Registering these deploy keys with your GitHub repo programmatically
- Configuring your new clone to use the appropriate deploy key while not conflicting with other 
SSH keys used elsewhere on your server
- ACL'ing these keys so they can be reused by people to fetch/deploy on your behalf
(and not readable by anyone else)

To get started, please wait for better instructions.

