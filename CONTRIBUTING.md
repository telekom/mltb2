# Contribution Guidelines

xyz

## Adding a new Feature

xyz

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

## Manage your Pull Request

- a new pull request should have the prefix `[WIP]` in its title: this indicates that you are still working on the PR

## Testing, Linting, and Formatting

xyz
