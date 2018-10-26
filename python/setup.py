import setuptools

long_description="""Plush is designed to SSH deploy keys on a remote computer using Fabric. These deploy keys are stored in the repo settings for your repo on GitHub using the GitHub API (using OAUTH credentials). Plush then clones your repo using a remote path that references these deploy keys. Plush allows multiple projects to have unique deploy keys all on one computer."""

setuptools.setup(name='plush-fabric',
      version='0.4.0',
      description='Helper library for Fabric to simplify creating and managing GitHub deploy keys when deploying GitHub-hosted repositories',
      long_description=long_description,
      author='Kevin Barnes',
      author_email='kbarnes3@gmail.com',
      url='https://github.com/kbarnes3/Plush',
      license='BSD',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'License :: OSI Approved :: BSD License',
          "Operating System :: OS Independent",
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          ],
      keywords='fabric github deployment',
      install_requires=['oauth2client>=3.0.0', 'PyGithub>=1.3.8', 'keyring>=12.0.0'],
      packages=['plush', 'plush.fabric_commands'],
      entry_points={
          'console_scripts': [
              'auth = plush.console:auth_entry',
              'listkeys = plush.console:list_keys_entry'
          ]
      },
      )
