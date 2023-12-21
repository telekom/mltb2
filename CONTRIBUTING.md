# How to contribute

This guide explains how you can contribute to this project. This can be in the form of a bug report or issue, for example, or as a feature in a pull request.

## Table of Contents

- [Report a Bug or Issue](#report-a-bug-or-issue)
- [Fix a Bug or add a new Feature](#fix-a-bug-or-add-a-new-feature)
- [Testing, Linting and Formatting](#testing-linting-and-formatting)
- [Code Style Guidelines](#code-style-guidelines)
- [Project Setup](#project-setup)

## Report a Bug or Issue

- We use GitHub issues to track bugs and feature requests.
- Please provide as much context as possible when you report a bug and open an issue.
- The information you provide should be comprehensive enough to reproduce the problem.
- Make sure the bug has not already been reported by searching the GitHub Issues.

## Fix a Bug or add a new Feature

### 1. Fork the Repository

- Go to the GitHub page of this project.
- Click the **Fork** button at the top right corner to create a copy of the project in your own GitHub account.

### 2. Clone the Forked Repository

- On your GitHub fork, click the **Code** button and copy the URL provided.
- Open your terminal or command prompt.
- Use the command `git clone [URL]` to clone the repository to your local machine.

### 3. Create a New Branch

- Navigate to the cloned directory (e.g., `cd project-name`).
- Create a new branch using `git checkout -b feature-branch-name` or your IDE.

### 4. Make Your Changes

- [Set up the project](#project-setup) if you have not already done so.
- Open the project in your code editor or IDE.
- Make your changes to the project.
- Test your changes to ensure they work correctly.
- Take note of chapter [Testing, Linting and Formatting](#testing-linting-and-formatting).
  This will avoid CI problems later on.
- Please adhere to the [Code Style Guidelines](#code-style-guidelines).
- Make sure that the code you add is your own or meets existing copyright guidelines.

### 5. Commit Your Changes

- After making changes, use `git add .` to stage all changes.
- Alternatively, to stage individual files, use `git add <file1> <file2> ...`.
- Commit the changes with `git commit -m "Add a meaningful commit message"`.
- Alternatively, you can of course also use your IDE for these steps.

### 6. Push to Your Fork

- Push the changes to your forked repository with `git push origin feature-branch-name`.
- Alternatively, you can of course also use your IDE for this.

### 7. Open a Pull Request

- Go to your forked repository on GitHub.
- Click the **Compare & pull request** button next to your `feature-branch-name`.
- Add a title and description for your pull request.
- A new pull request should have the prefix `[WIP]` (work in progress) in its title:
  this indicates that you are still working on the PR.
- Click **Create pull request**.
- Check the results of the CI checks and make corrections if necessary.
- When the pull request is finished from your point of view, remove the `[WIP]` prefix.
  Then write a short comment that you are finished with the PR and it can be reviewed.
- By submitting your pull request, you place the code you add
  under the copyright conditions of this project.

### 8. Await Review

- Once the pull request is open, maintainers of the original repository will review your changes.
- Engage in any discussions and make necessary changes if requested.

### 9. Merge the Pull Request

- After your pull request is approved, a maintainer will merge it into the project.
- Congratulations, you’ve successfully contributed to the project!

### Additional Tips:

- Always pull the latest changes from the original repository to your fork main branch
  before starting a new feature.
- More helpful resources:
  - GitHub Docs: [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
  - GitHub Docs: [Contributing to a project](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project)

## Testing, Linting and Formatting

We use different formatters and linters in this project.
You can use them to format the code or just to check or test the code.

This project is using [GitHub Actions](https://docs.github.com/en/actions)
to execute all checks and tests in a CI pipeline.
To save time you can and should execute those tests in your locale development environment.

In this project we are using the Make tool.
If you are on Windows either change to a proper operating system
or execute the individual commands that can be found in `Makefile`.

- to run all code formatters use: `make format`
- to run all checks use: `make check`
- to run all tests use: `make test` or your preferred IDE

## Code Style Guidelines

- code must be compatible with all Python versions configured in `pyproject.toml` (see `python =`)
- max line length is 119
- Docstrings
  - use [Google docstring format](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
  - this is integrated with [Sphinx](https://www.sphinx-doc.org/) using the
    [napoleon extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
- versioning: use [Semantic Versioning Specification](https://semver.org/) and
  [PEP 440 (Version Identification and Dependency Specification)](https://www.python.org/dev/peps/pep-0440/)
- All Python modules must have an appropriate copyright header.

## Project Setup

We recommend to do the setup in a text console and not with a GUI tool.
This offers better controle and transparency.

We use [Poetry](https://python-poetry.org/docs/) and
[pyenv](https://github.com/pyenv/pyenv). Not Conda, Anaconda or direct pip.

### 1. Get Project Source

First you have to clone the project with GIT.
If you want to make a pull request, you must clone your previously forked project and
not the original project.
After the project has been cloned, use `cd` to change into the project directory.

### 2. Install Poetry

We use [Poetry](https://python-poetry.org/docs/) for dependency management and packaging in this project.
The next step is the [installation of Poetry](https://python-poetry.org/docs/#installation),
if you do not already have it.
Poetry offers different installation options. We recommend the option "with the official installer".
But it does not matter. It's your choice.

### 3. Configure Poetry

We suggest the following two config options. These are not mandatory but useful.

Set [`virtualenvs.prefer-active-python`](https://python-poetry.org/docs/configuration/#virtualenvsprefer-active-python-experimental)
to `true`.
With this setting Poetry uses the currently activated Python version to create a new virtual environment.
If set to false, the Python version used during Poetry installation is used.
This makes it possible to determine the exact Python version for development.
This can be done [global or locale](https://python-poetry.org/docs/configuration/#local-configuration).
We suggest to do this setting as global.

- global setting: `poetry config virtualenvs.prefer-active-python true`
- locale setting: `poetry config virtualenvs.prefer-active-python true --local` - this will create or change the `poetry.toml` file

Set [`virtualenvs.options.always-copy`](https://python-poetry.org/docs/configuration/#virtualenvsoptionsalways-copy)
to `true`.
When the new virtual environment is created (later) all needed files are copied into it instead of symlinked.
The advantage is that you can delete the old globally installed Python version later without breaking the Python in
the locale virtual environment.
The disadvantage is that we waste some disk space.
This can be done [global or locale](https://python-poetry.org/docs/configuration/#local-configuration).
We suggest to do this setting as global.

- global setting: `poetry config virtualenvs.options.always-copy true`
- locale setting: `poetry config virtualenvs.options.always-copy true --local` - this will create or change the `poetry.toml` file

### 4. Set the Python Version (pyenv)

We recommend [pyenv](https://github.com/pyenv/pyenv) to install and manage different Python versions.
First [install pyenv](https://github.com/pyenv/pyenv#installation) if you do not already have it.

Next install the appropriate Python version.
We recommend the development on the oldest still permitted Python version of the project.
This version number can be found in the `pyproject.toml` file in the setting called
`tool.poetry.dependencies.python`. If this is set like `python = "^3.8"`
we use pyenv to install Python 3.8:
`pyenv install 3.8`
This installs the latest 3.8 Python version.

If the Python installation was successful we use `pyenv versions` to see which exact Version is installed.
Then we activate this version with `pyenv local <version>`.
This command will create a `.python-version` file in the project directory.
Make sure that you are still in the project directory.
For example execute: `pyenv local 3.8.17`

### 5. Install the Project with Poetry

Execute `poetry install --all-extras` to install the project.
This installs all dependencies, optional (extra) dependencies and
needed linting, testing and documentation dependencies.
With this method, the sources are also implicitly installed in
[editable mode](https://pip.pypa.io/en/latest/cli/pip_install/#cmdoption-e).
