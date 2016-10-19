from distutils.core import setup


setup(name='fabricghdeploykeys',
      version='1.0.0',
      description='Helper library for Fabric to simplify creating and managing GitHub deploy keys when deploying GitHub-hosted repositories',
      author='Kevin Barnes',
      author_email='kbarnes3@gmail.com',
      url='https://github.com/kbarnes3/FabricGHDeployKeys',
      install_requires=['oauth2client>=3.0.0', 'PyGithub>=1.28', 'keyring>=9.3.1'],
      packages=['fabricghdeploykeys', 'fabricghdeploykeys.fabric_commands'],
      entry_points={
          'console_scripts': [
              'auth = fabricghdeploykeys.console:auth_entry',
              'listkeys = fabricghdeploykeys.console:list_keys_entry'
          ]
      },
      )
