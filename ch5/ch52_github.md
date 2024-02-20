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

# 5.2 Software Versioning
```{code-cell} bash
:tags: [remove-input]
cd ../home
mkdir ch52
cd ch52
```

## What is Versioning?

Versioning is the process of assigning unique version numbers to distinct states of software projects, allowing developers and users to track progress, manage changes, and ensure compatibility between different components. It plays a critical role in software development and release management, offering a structured way to reflect the history, stability, and compatibility of software products over time. Through versioning, teams can effectively communicate the impact of changes, manage dependencies, and facilitate the adoption of new features while maintaining the integrity of existing systems.

## What is Semantic Versioning?

Semantic Versioning, often abbreviated as SemVer, is a versioning scheme that aims to convey meaning about the underlying changes in a release through the version number itself. Defined by [Semantic Versioning 2.0.0](https://semver.org/), it adopts a structured format of `MAJOR.MINOR.PATCH` to differentiate between the types of changes made to a project:

- **MAJOR** version when you make incompatible API changes,
- **MINOR** version when you add functionality in a backward-compatible manner, and
- **PATCH** version when you make backward-compatible bug fixes.

Additional labels for pre-release and build metadata are available as extensions to the `MAJOR.MINOR.PATCH` format.

The principles of Semantic Versioning help ensure a consistent, predictable approach to versioning that is directly tied to the significance of the changes made. It allows developers and consumers of software to make informed decisions about upgrading and integrating with other systems. By adhering to SemVer, projects can communicate the nature of changes efficiently, reduce the potential for conflicts, and facilitate easier dependency management in the complex ecosystem of software development.

# Automate Semantic Versioning in Poetry Projects with Python Semantic Release

Using `python-semantic-release` to automate semantic versioning in projects managed with Poetry on GitHub involves setting up `python-semantic-release` in your project, configuring it to work with Poetry, and automating the release process through GitHub Actions.

## Prerequisites

- A GitHub repository with a Python project managed by Poetry.
- Basic understanding of semantic versioning, Git, and GitHub Actions.

## Setup Your Python Project with Poetry

Ensure your project is set up with Poetry and has a `pyproject.toml` file at its root. This file should define your project's dependencies and metadata. If your project isn't set up with Poetry yet, you can start by running:

```{code-block} bash
poetry init
```

And follow the prompts to create your `pyproject.toml`.

In this section, we will use the `poetry-demo` project.

```{code-cell} bash
poetry new poetry-demo
```

Navegate to the root folder of the project.

```{code-cell} bash
cd poetry-demo
```

## Change the Python Versions Supported by the Project

Since `python-semantic-release` requires `Python >=3.8`, before installing python-semantic-release, it is important that 
you check and change the Python version supported by the project.
In the `pyproject.toml` file, look for:

```toml
[tool.poetry.dependencies]
python = "^3.7"
```

Change it to: 

```toml
[tool.poetry.dependencies]
python = "^3.8"
```

```{code-cell} bash
:tags: [remove-input]
sed -i 's/python = "^3.7"/python = "^3.8"/' pyproject.toml
```

## Install Python Semantic Release

Add `python-semantic-release` to your development dependencies using Poetry. This ensures that the semantic release process is part of your development workflow.

```{code-cell} bash
:tags: [scroll-output]
poetry add --group dev python-semantic-release
```

## Configure Python Semantic Release

Create a configuration file for `python-semantic-release` in your project's root directory. You can either use a `.toml` file (e.g., `pyproject.toml`) or a `.semantic-release.toml` file for configuration.

If you're using `pyproject.toml`, add the following configuration under `[tool.semantic_release]`:

```toml
[tool.semantic_release]
version_variable = "pyproject.toml:version"
commit_version_number = true
upload_to_pypi = "false"
```

```{code-cell} bash
:tags: [remove-input]
echo >> pyproject.toml
echo '[tool.semantic_release]' >> pyproject.toml
echo 'version_variable = "pyproject.toml:version"' >> pyproject.toml
echo 'commit_version_number = true' >> pyproject.toml
echo 'upload_to_pypi = "false"' >> pyproject.toml
```

## Setup GitHub Actions for Continuous Deployment

To automate the release process, you'll use GitHub Actions. Create a `.github/workflows/release.yml` file in your repository with the following content:

```{code-block} yaml
name: Semantic Release

on:
  push:
    branches:
      - main

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency: release
    permissions:
      id-token: write
      contents: write

    steps:
    - uses: actions/setup-python@v4
      with:
        python-version: 3.11
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    - name: Python Semantic Release
      run: |
        pip install python-semantic-release
        semantic-release version
        semantic-release publish
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

```{code-cell} bash
:tags: [remove-input]
mkdir -p .github/workflows/
touch .github/workflows/release.yml
echo 'name: Semantic Release

on:
  push:
    branches:
      - main

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency: release
    permissions:
      id-token: write
      contents: write

    steps:
    - uses: actions/setup-python@v4
      with:
        python-version: 3.11
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    - name: Python Semantic Release
      run: |
        pip install python-semantic-release
        semantic-release version
        semantic-release publish
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}' >> .github/workflows/release.yml
```
## Create a new repository 

Create a new empty repository in Github and name it `semver`.

```{code-cell} bash
:tags: ["remove-input","remove-output"]
/home/callaram/.conda/envs/jupyterbook/bin/gh repo create semver --public
```

## Commit and Push Your Changes

After configuring everything, commit your changes (including the `pyproject.toml` modifications and GitHub Actions workflow) and push them to your GitHub repository.

```{code-cell} bash
git init
git add .
git commit -m "feat(semver): Setup semantic release"
git branch -M main
git remote add origin git@github.com:mcallara/semver.git
git push -u origin main
```

## Make Semantic Commits

To ensure `python-semantic-release` correctly increments version numbers, use semantic commit messages (e.g., `fix:`, `feat:`, `BREAKING CHANGE:`) for your commits. This practice helps the tool to automatically determine the next version number based on the changes made.

```{admonition} What to notice
:class: hint

After pushing our first commit and successfully running `python-semantic-release`, the tool will automatically generate both a release and a tag for your project, as well as a `CHANGELOG.md` file. You can find the generated release in the [Releases section](https://github.com/mcallara/semver/releases) of the `semver` repository. This section provides detailed information about what's new, improved, or fixed in each release, along with any associated assets.

Similarly, the automatically created tag, marking the specific point in the repository's history for the release, can be found in the [Tags section](https://github.com/mcallara/semver/tags). Tags serve as important reference points, indicating version releases and facilitating easy navigation through the project's version history.
```

% Teardown
%```{code-cell} bash
%gh repo delete semver --yes
%```