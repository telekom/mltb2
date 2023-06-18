# Copyright (c) 2021 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Build script for setuptools."""

import os

import setuptools


files_requires = {"platformdirs", "scikit-learn"}
fasttext_requires = files_requires | {"fasttext-wheel"}
optuna_requires = {"numpy", "optuna", "scipy"}
plot_requires = {"matplotlib"}
somajo_requires = {"SoMaJo", "tqdm"}
transformers_requires = {"scikit-learn", "torch", "tqdm", "transformers"}
somajo_transformers_requires = somajo_requires | transformers_requires | {"tqdm"}
optional_requires = (
    somajo_transformers_requires
    | transformers_requires
    | somajo_requires
    | plot_requires
    | optuna_requires
    | fasttext_requires
    | files_requires
)

project_name = "mltb2"
source_code = "https://github.com/telekom/mltb2"
keywords = "optuna deep-learning ml ai machine-learning hyperparameter-optimization"
install_requires = ["numpy", "scipy", "tqdm"]
extras_require = {
    "files": files_requires,
    "fasttext": fasttext_requires,
    "optuna": optuna_requires,
    "plot": plot_requires,
    "somajo": somajo_requires,
    "transformers": transformers_requires,
    "somajo_transformers": somajo_transformers_requires,
    "optional": optional_requires,
    "checking": [
        "black",
        "flake8",
        "isort",
        "mdformat",
        "pydocstyle",
        "mypy",
        "pylint",
        "pylintfileheader",
    ],
    "testing": ["pytest", "packaging"],
    "doc": ["sphinx", "sphinx_rtd_theme", "myst_parser", "sphinx_copybutton"],
}

# add "all"
all_extra_packages = list(
    {package_name for value in extras_require.values() for package_name in value}
)
extras_require["all"] = all_extra_packages


def get_version():
    """Read version from ``__init__.py``."""
    version_filepath = os.path.join(os.path.dirname(__file__), project_name, "__init__.py")
    with open(version_filepath) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.strip().split()[-1][1:-1]
    assert False


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=project_name,
    version=get_version(),
    maintainer="Philip May",
    author="Philip May",
    author_email="philip@may.la",
    description="Machine Learning Toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=source_code,
    project_urls={
        "Bug Tracker": source_code + "/issues",
        "Documentation": "https://telekom.github.io/mltb2/",
        "Source Code": source_code,
        # "Contributing": source_code + "/blob/main/CONTRIBUTING.md",
        # "Code of Conduct": source_code + "/blob/main/CODE_OF_CONDUCT.md",
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require=extras_require,
    keywords=keywords,
    classifiers=[
        "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        # "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
)
