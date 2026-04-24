---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Bash
  language: bash
  name: bash
---
% Sections:
%Packaging (https://packaging.python.org/en/latest/flow/ , https://python-poetry.org/docs/libraries/ )
%Distribution package
%What is a distribution package
%Build with poetry
%Python Package Index (PyPI)
%Upload to the package distribution service, publishing with poetry.
% Create Github account
% In this section, we will learn to use Poetry to build and publish our Python package to the Python Package Index (PyPI). 
% We will use the Github Actions CI/CD pipeline to automate the build and publish process.
% We will continue our work with the `poetry-demo` project. Since, in the previous section, we added a PYPI_TOKEN variable to our repo, you don't need to do it again.

# 5.3 Packaging
```{code-cell} bash
:tags: [remove-input]
cd ../home/ch5/my-package
```
In this chapter, we'll explore the essentials of Python packages, package registries, and how to utilize Poetry for package management. Additionally, we will delve into automating the build and publish process using the GitHub Actions CI/CD pipeline, by continuing our work with the `poetry-demo` project.

## Python Packages

A Python Package is a collection of modules that are bundled together. These packages can be easily distributed for use in other projects, promoting code reuse and modular programming. Python packages can include libraries, frameworks, or collections of code and resources for specific purposes.

If we look at the structure of our `my-package` project, and compare it with the structure of the flat layout we will notice that we are missing the folder that is supposed to contain the code of our package. 

To transform our repository in a real python package, let's create a new folder named `my_package` and add an `__init__.py` file into it.

```{code-cell} bash
:tags: [remove-input]
mkdir my_package
cd my_package
touch __init__.py
```

## Package Registries

A Package Registry is a storage space for packages where they can be published, shared, and managed. It allows developers to easily distribute and install packages using package management tools. The Python Package Index (PyPI) is the standard registry for Python packages. Organizations may also use private registries for internal tools and libraries.

## Publishing Python packages with PyPI

While GitHub Packages supports several formats, it does **not** support Python packages (PyPI) as a native registry. Therefore, to distribute Python packages, you should use the Python Package Index (PyPI).

## Building and Publishing with Poetry

To publish a package to PyPI, you need to create a package distribution file. This file contains the package's code, resources, and metadata, and can be installed using package management tools. Poetry offers a command to build the package distribution files: `poetry build`.

Once the distribution files are created, you can publish the package to PyPI using the `poetry publish` command.

## Automating Build and Publish with GitHub Actions

We can automate the build and publish process using the GitHub Actions CI/CD pipeline. This allows us to build and publish the package to PyPI whenever a new version is released, without manual intervention.

To achieve this we will add a `publish` job to our workflow file in `.github/workflows/`.

### Adding the Publish job

Below is the configuration for the `publish` job in a GitHub Actions workflow file (e.g., `.github/workflows/publish.yml`). This job runs on pushes to the default branch and triggers when a commit message follows semantic versioning.

```yaml
# .github/workflows/publish.yml
name: Publish Python Package

on:
  push:
    branches:
      - main
    # Optionally, filter by commit message using a workflow condition

jobs:
  publish:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, '.') # simple check for version-like commit
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install Poetry
        run: pip install poetry
      - name: Build package
        run: poetry build
      - name: Publish to PyPI
        run: |
          poetry config pypi-token.pypi ${{ secrets.PYPI_TOKEN }}
          poetry publish --build
        env:
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

This configuration does the following:

1. Checks out the code and sets up Python.
2. Installs Poetry.
3. Builds the package using `poetry build`.
4. Publishes the package to PyPI using `poetry publish`.

You must ensure that `PYPI_TOKEN` is available in your repository secrets. You can generate this token from your PyPI account and add it to your GitHub repository secrets.

### Installing packages from PyPI with `pip`

To install a package from a registry, `pip` is commonly used. For example, to install a package named `example-package` from PyPI, you would use:

```bash
pip install example-package
```

`pip` searches for the package in PyPI (or another configured registry), downloads it, and installs it in your Python environment.

To install your published package from PyPI, use:

```bash
pip install poetry-demo
```