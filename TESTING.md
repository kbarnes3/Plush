Testing
=======

Setup
-----
First, set up a clean Ubuntu 18.04 LTS server VM. Update it by running:
  * `sudo apt-get update`
  * `sudo apt-get dist-upgrade`
  * `sudo apt-get autoremove`
  * `sudo reboot`

Make a note of your VM's IP address by running `ifconfig`

At this point, it's recommended to take a snapshot or checkpoint of the VM to make repeated testing easier.

The next steps are easiest to run in a PowerShell prompt that has run `scripts\Console.ps1`. These steps will exercise most of the functionality that Plush offers.

1. Clear any cached GitHub OAuth credentials by running `auth delete`.
1. Get new credentials by running `auth`.
1. Confirm the credentials by running `auth verify`. Your GitHub username (and maybe other information depending on your privacy settings) should be displayed.
1. Run `Fabric-SetupUser -Hosts username@ip_address -User username -PublicKeyFile Path\To\id_rsa.pub -NoSudoPasswd -PromptForLoginPassword -PromptForSudoPassword`. Use the same username in both fields to test setting up an existing user on the server appropriately
1. Run `Fabric-SetupUser -Hosts username@ip_address -User new_username -PublicKeyFile Path\To\id_rsa.pub -NoSudoPasswd [-PromptForPassphrase]`. This tests creating a new user account as well as authenticating with a key file instead of a password. `-PromptForPassphrase` is only needed if your private key has a password set and you aren't using an SSH agent. It makes things easier if you pass the same public key in for the new account.
1. Run `Fabric-TestDeploy -Hosts username@ip_addres -Repo "githubname/Repo" [-PromptForPassphrase]` where `username` is the initial account you set up and `githubname/Repo` is a valid GitHub repo that you control. It can be either public or private. For example, I can pass `kbarnes3/Plush` here, but that will fail for anyone else as they don't have permission to add a deploy key to this repo.
1. SSH in to your test VM and confirm the repo was cloned to `/var/src/test/`.
1. Run `Fabric-TestDeploy -Hosts new_username@ip_addres -Repo "githubname/AnotherRepo" [-PromptForPassphrase]` where `new_username` is the second account you created. It's easiest to verify this works by providing a different repo than you cloned previously.
1. SSH in to your test VM and confirm the repo was cloned to `/var/src/test/`.
1. Log into GitHub and delete any deploy keys you don't need on the repos you used.

If all of these steps worked successfully, you have verified the core functionality of Plush!
