Setup Your Development Enviroment
=================================

These directions currently assume your ideal dev environment is on Windows using PowerShell. Other configurations are possible, but not yet documented.

This project uses PowerShell scripts based on GitHub's [Scripts To Rule Them All](https://github.com/github/scripts-to-rule-them-all) to make common developer flows easier.

To setup your dev environment
-----------------------------

1. Install all the required tools. This includes:  
    a. The latest release of [Python 3.6](https://www.python.org/). Other versions of Python are not currently tested. Python 3.6 is used as it is the default version installed on Ubuntu 18.04 LTS.
    b. The latest release of [Git](http://git-scm.com/downloads).
1. Clone the repo locally and open a PowerShell prompt in the root folder.
1. Run scripts\Console.ps1. The first time this script is run, it will create a virtual env and install dependencies such as Fabric.

After the initial setup
-----------------------

1. After the initial setup, run scripts\Console.ps1 to reenter your virtual env and ensure it is up to date. Console.ps1 takes an optional -Quick flag to skip most update checks. Console.ps1 also defines a few helpful functions in your PowerShell environment:  
    Invoke-Fabric: calls [Fabric](https://www.fabfile.org/) with the given arguments  
    Update-DevEnvironment: calls scripts\Update.ps1 (see below for more details)
1. After pulling/merging/etc. it's a good idea to run Update-DevEnvironmnet or scripts\Update.ps1 to ensure any new or updated dependencies are setup correctly.
1. The fabfile.py contains example functions that demonstrate the usage of Plush. Running setup_user or test_deploy will exercise a lot of the functionality of this project.
1. If you want to reset your local repo back to a clean state, run scripts\Setup.ps1 -GitClean. Be warned that this will delete a lot of files, such as any untracked files and your venv.
