from distutils.core import setup

# This private version of PyGithub merges in a pull request to add support for read-only deploy keys
# This can be changed back to the mainline releases once https://github.com/PyGithub/PyGithub/pull/467 is merged
# or issue https://github.com/PyGithub/PyGithub/issues/405 is fixed some other way
pygithub = 'https://github.com/kbarnes3/PyGithub/archive/v1.30.private.zip#egg=PyGithub-1.30.private+git.877cd76'

setup(name='fabricghdeploykeys',
      version='1.0.0',
      description='Helper library for Fabric to simplify creating and managing GitHub deploy keys when deploying GitHub-hosted repositories',
      author='Kevin Barnes',
      author_email='kbarnes3@gmail.com',
      url='https://github.com/kbarnes3/FabricGHDeployKeys',
      install_requires=['oauth2client>=3.0.0', 'PyGithub==1.30.private+git.877cd76', 'keyring>=9.3.1', ],
      dependency_links=[pygithub, ],
      packages=['fabricghdeploykeys', 'fabricghdeploykeys.fabric_commands'],
      entry_points={
          'console_scripts': [
              'auth = fabricghdeploykeys.console:auth_entry',
              'listkeys = fabricghdeploykeys.console:list_keys_entry'
          ]
      },
      )
