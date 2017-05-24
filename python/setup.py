from distutils.core import setup

# This private version of PyGithub merges in a pull request to add support for read-only deploy keys
# This can be changed back to the mainline releases once https://github.com/PyGithub/PyGithub/pull/467 is merged
# or issue https://github.com/PyGithub/PyGithub/issues/405 is fixed some other way
pygithub = 'https://github.com/kbarnes3/PyGithub/archive/v1.30.private.zip#egg=PyGithub-1.30.private'

setup(name='plush',
      version='0.1.0',
      description='Helper library for Fabric to simplify creating and managing GitHub deploy keys when deploying GitHub-hosted repositories',
      author='Kevin Barnes',
      author_email='kbarnes3@gmail.com',
      url='https://github.com/kbarnes3/Plush',
      install_requires=['oauth2client>=3.0.0', 'PyGithub==1.34', 'keyring>=9.3.1', ],
      dependency_links=[pygithub, ],
      packages=['plush', 'plush.fabric_commands'],
      entry_points={
          'console_scripts': [
              'auth = plush.console:auth_entry',
              'listkeys = plush.console:list_keys_entry'
          ]
      },
      )
