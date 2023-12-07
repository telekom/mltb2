# Contribution Guidelines

xyz

## Adding a new Feature

xyz

## Testing, Linting, and Formatting

We use different formatters and linters in this project.
You can use them to format the code or just to check the code.

In this project we are using the Make tool.
If you are on Windows either change to a proper operating system
or execute the individual commands that can be found in `Makefile`.

- to run all code formatters use: `make format`
- to run all checks use: `make check`
- to run all tests use: `make test` or your preferred IDE

## Project Setup

We recommend to do the setup in a text console and not with a GUI tool.
This offers better controle and transparency.

### Get Project Source

First you have to clone the project with GIT.
After the project has been cloned, use `cd` to change into the project directory.

### Install Poetry

We use [Poetry](https://python-poetry.org/docs/) for dependency management and packaging in this project.
The next step is the [installation of Poetry](https://python-poetry.org/docs/#installation),
if you do not already have it.
Poetry offers different installation options. We recommend the option "with the official installer".
But it does not matter. It's your choice.

### Configure Poetry

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

### Set the Python Version (pyenv)

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

### Install Project with Poetry

Execute `poetry install --all-extras` to install the project.
This installs all dependencies, optional (extra) dependencies and
needed linting, testing and documentation dependencies.
With this method, the sources are also implicitly installed in
[editable mode](https://pip.pypa.io/en/latest/cli/pip_install/#cmdoption-e).

## Manage your Pull Request

- a new pull request should have the prefix `[WIP]` in its title: this indicates that you are still working on the PR
