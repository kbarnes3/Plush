import setuptools

description = "Helper library for Fabric to simplify creating and managing GitHub deploy keys when deploying " \
              "GitHub-hosted repositories"

long_description = open('README.rst').read()

setuptools.setup(name='plush-fabric',
                 version='0.5.1',
                 description=description,
                 long_description=long_description,
                 author='Kevin Barnes',
                 author_email='kbarnes3@gmail.com',
                 url='https://github.com/kbarnes3/Plush',
                 license='BSD',
                 classifiers=[
                     'Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'Topic :: Software Development',
                     'License :: OSI Approved :: MIT License',
                     "Operating System :: OS Independent",
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.6',
                 ],
                 keywords='fabric github deployment',
                 install_requires=['oauth2client>=3.0.0', 'PyGithub>=1.3.8', 'keyring>=12.0.0', 'fabric>=2.5.0',
                                   'patchwork>=1.0.1'],
                 packages=['plush', 'plush.fabric_commands'],
                 entry_points={
                     'console_scripts': [
                         'auth = plush.console:auth_entry',
                         'listkeys = plush.console:list_keys_entry'
                     ]
                 },
                 )
