# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Configuration for the Sphinx documentation builder."""

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from typing import List

# -- Project information -----------------------------------------------------

project = "MLTB2"
copyright = "2023, Philip May, Deutsche Telekom AG"  # noqa: A001
author = "Philip May"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",  # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
    "sphinx_rtd_theme",  # https://github.com/readthedocs/sphinx_rtd_theme
    "sphinx.ext.napoleon",  # https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
    "sphinx.ext.viewcode",  # https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html
    # "recommonmark",
    # "myst_parser",  # https://myst-parser.readthedocs.io/
    "sphinx.ext.intersphinx",  # https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
    "sphinx_copybutton",  # https://github.com/executablebooks/sphinx-copybutton
    "sphinx.ext.todo",  # https://www.sphinx-doc.org/en/master/usage/extensions/todo.html
    "sphinx.ext.doctest",  # https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- additional settings -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    # "transformers": ("https://huggingface.co/transformers/", None),
    "optuna": ("https://optuna.readthedocs.io/en/stable/", None),
    "mlflow": ("https://www.mlflow.org/docs/latest/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "git": ("https://gitpython.readthedocs.io/en/stable/", None),
    "platformdirs": ("https://platformdirs.readthedocs.io/en/latest/", None),
    "arango": ("https://docs.python-arango.com/en/main/", None),
    # "matplotlib": ("https://matplotlib.org/stable/", None),
}

# html_logo = "imgs/xxx.png"

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    "css/custom.css",
]

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# add github link
html_context = {
    "display_github": True,
    "github_user": "telekom",
    "github_repo": "mltb2",
    "github_version": "main/docs/source/",
}

source_suffix = [".rst", ".md"]

# -- autosummary config -------------------------------------------------
# This value controls how to represent typehints.
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_typehints
autodoc_typehints = "both"

# This value selects what content will be inserted into the main body of an autoclass directive.
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autoclass_content
# autoclass_content = "both"

# The default options for autodoc directives.
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_default_options
autodoc_default_options = {
    # If set, autodoc will generate document for the members of the target module, class or exception.
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-option-automodule-members
    "members": True,
    "show-inheritance": True,
    # If set, autodoc will also generate document for the special members (that is, those named like __special__).  # noqa: E501
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-option-automodule-special-members
    "special-members": None,
    # If set, autodoc will also generate document for the private members (that is, those named like _private or __private).  # noqa: E501
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#directive-option-automodule-private-members
    "private-members": None,
    "exclude-members": "__weakref__, __init__, __repr__, __post_init__, __hash__, __eq__",
}

# True to convert the type definitions in the docstrings as references.
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#confval-napoleon_preprocess_types
napoleon_preprocess_types = True

# True to parse NumPy style docstrings. False to disable support for NumPy style docstrings.
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#confval-napoleon_numpy_docstring
napoleon_numpy_docstring = False

# If this is True, todo and todolist produce output, else they produce nothing. The default is False.
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#confval-todo_include_todos
todo_include_todos = True
