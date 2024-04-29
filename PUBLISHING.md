Publishing to PyPI
=================

These directions are only meaningful for people with write access to the [plush-fabric package on PyPI](https://pypi.org/project/plush-fabric/). Publishing Plush uses the automated CI/CD flow for GitHub Actions described [here](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/).

Any changes to the `trunk` branch should automatically publish a package to [TestPyPi](https://test.pypi.org/manage/project/plush-fabric/).
If this isn't working, official PyPi releases are also likely broken.

To create a new PyPi release:

1. Create a new branch and rev the version number following semantic versioning guidelines.
1. Create a pull request for this branch and make sure all the checks in Azure Pipelines pass before completing. See CONTRIBUTING.md for more details.
1. Create the pull request
1. Checkout the trunk branch locally and make sure the latest changes are pulled
1. Run `git tag v*version*`.
1. Run `git push origin v*version*`.
1. The GitHub Actions defined in `.github\workflows\release.yml` will run.
   These will build the Python wheel, upload it to PyPi, and create the release on GitHub.
1. Go to GitHub and describe the notable changes in the release section.
