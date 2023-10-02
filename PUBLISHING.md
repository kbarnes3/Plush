Publishing to PyPI
=================

These directions are only meaningful for people with write access to the [plush-fabric package on PyPI](https://pypi.org/project/plush-fabric/). Publishing Plush uses the standard flow described [here](https://packaging.python.org/tutorials/packaging-projects/), but the directions are maintained here as well for consistency.

These steps should all be followed in a console set up as described in Setup-Dev-Environment.md. Unless specified, they should all be run in the `python` directory.

1. Create a new branch and rev the version number following semantic versioning guidelines.
1. Create a pull request for this branch and make sure all the checks in Azure Pipelines pass before completing. See CONTRIBUTING.md for more details.
1. Switch to trunk and merge in this pull request.
1. Run `python -m build --sdist --wheel`.
1. Run `twine upload dist/*version*`.
1. Confirm the new package is visible on [PyPi](https://pypi.org/project/plush-fabric/).
1. Run `git tag v*version*`.
1. Run `git push origin v*version*`.
1. Go to GitHub and describe the notable changes in the release section.
