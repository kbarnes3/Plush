from distutils.core import setup


setup(name='fabricghdeploykeys',
      version='1.0.0',
      description='Helper library for Fabric to simplify creating and managing GitHub deploy keys when deploying GitHub-hosted repositories',
      author='Kevin Barnes',
      author_email='kbarnes3@gmail.com',
      url='https://github.com/kbarnes3/FabricGHDeployKeys',
      install_requires=['oauth2client>=3.0.0', 'PyGithub>=1.28', 'keyring>=9.3.1'],
      packages=['fabricghdeploykeys'],
      entry_points={
          'console_scripts': [
              'auth = fabricghdeploykeys.oauth_flow:run_oauth_flow'
          ]
      },
      )
