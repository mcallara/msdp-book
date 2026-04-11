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

% Ensure that my-package exist in Gitlab before running with a valid GITLAB_TOKEN

# 5.2 Software Versioning
```{code-cell} bash
:tags: ["remove-input","remove-output"]
cd ../home
mkdir ch5
cd ch5
git clone git@gitlab.com:msdp.book/my-package.git
cd my-package
```

## What is Versioning?

Versioning is the process of assigning unique version  to distinct states of software projects, allowing developers and users to track progress, manage changes, and ensure compatibility between different components. It plays a critical role in software development and release management, offering a structured way to reflect the history, stability, and compatibility of software products over time. Through versioning, teams can effectively communicate the impact of changes, manage dependencies, and facilitate the adoption of new features while maintaining the integrity of existing systems.

## What is Semantic Versioning?

Semantic Versioning, often abbreviated as SemVer, is a versioning scheme that aims to convey meaning about the underlying changes in a release through the version number itself. Defined by [Semantic Versioning 2.0.0](https://semver.org/), it adopts a structured format of `MAJOR.MINOR.PATCH` to differentiate between the types of changes made to a project:

- **MAJOR** version when you make incompatible API changes,
- **MINOR** version when you add functionality in a backward-compatible manner, and
- **PATCH** version when you make backward-compatible bug fixes.

Additional labels for pre-release and build metadata are available as extensions to the `MAJOR.MINOR.PATCH` format.

The principles of Semantic Versioning help ensure a consistent, predictable approach to versioning that is directly tied to the significance of the changes made. It allows developers and consumers of software to make informed decisions about upgrading and integrating with other systems. By adhering to SemVer, projects can communicate the nature of changes efficiently, reduce the potential for conflicts, and facilitate easier dependency management in the complex ecosystem of software development.

## Automate Semantic Versioning in Poetry Projects with Python Semantic Release

We can use a python package called `python-semantic-release` to automate semantic versioning in projects managed with Poetry on Gitlab. This package automates the process of determining the next version number based on the changes made to the project, generating release notes, and publishing the release to a repository. By integrating `python-semantic-release` with Gitlab CI/CD, we can automate the entire release process, ensuring that version numbers are incremented correctly and that releases are published consistently.

## Automating the semantic versioning of My Package

Let's see how to automate semantic versioning in a Python project managed with Poetry using `python-semantic-release` and Gitlab CI/CD. We will use the `my-package` project that we created in the previous section and configure it to use `python-semantic-release` for versioning and release management.

## Creating a personal access token

To allow `python-semantic-release` to interact with your Gitlab repository, you need to create a personal access token. This token will be used to authenticate the tool when it performs actions such as creating releases and tags.

To create a new personal access token, go to your GitLab account Preferences and click on ["Access Tokens"](https://gitlab.com/-/user_settings/personal_access_tokens) in the "User Settings" section. Then, click on "Add new token" and fill in the required details.
You can use:
- Token name: semantic_release
- Check the following scopes: `api`, `read_user`, `read_repository`, and `write_repository`. Once you've created the token, copy it to your clipboard, as you'll need it later.

## Adding the token to the GitLab CI/CD variables

To add the token to the GitLab CI/CD variables, go to the settings of the repository and then to the [CI/CD section](https://gitlab.com/msdp.book/semver/-/settings/ci_cd). Browse until you find the "Variables" section and click on "Expand" to reveal the form for adding a new variable. Now click on "Add variable" and add a new variable with:

- Type: Variable (default)
- Environment: All (default)
- Protect Variable, Mask Variable, Expand variable reference
- Key: GITLAB_TOKEN
- Value: `<your token>`

## Setup Your Python Project with Poetry

To ensure that our project is set up with Poetry and has a `pyproject.toml` file at its root, we need to initialize the project using Poetry. 

Let's now initialize the poetry project in the `my-package` directory by running the following command inside the directory:

```{code-block} bash
poetry init
```

```{code-cell} bash
:tags: [remove-input]
echo $'[tool.poetry]
name = "my-package"
version = "0.1.0"
description = ""
authors = ["msdp-book <msdp.book@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.8"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
' >> pyproject.toml
```

## Change the Python Versions Supported by the Project

Since `python-semantic-release` requires `Python >=3.8`, before installing python-semantic-release, it is important that you check and change, if needed, the Python version supported by the project.
In the `pyproject.toml` file, look for the section `[tool.poetry.dependencies]` and change the Python version to `^3.8` if a lower version is specified.

For example, if you find:

```{code-block} toml
[tool.poetry.dependencies]
python = "^3.7"
```

Change it to: 

```{code-block}  toml
[tool.poetry.dependencies]
python = "^3.8"
```

```{code-cell} bash
:tags: [remove-input]
sed -i 's/python = "^3.7"/python = "^3.8"/' pyproject.toml
```

## Add Python Semantic Release as a dependency of your project

Add `python-semantic-release` to your development dependencies using Poetry.

```{code-cell} bash
:tags: [scroll-output]
poetry add --group dev python-semantic-release
```

## Configure Python Semantic Release

To configure `python-semantic-release`, we will use the `pyproject.toml`. We will add two sections to the file: `[tool.semantic_release]` and `[tool.semantic_release.remote]`. The first section will define the version variable, whether to commit the version number, and whether to upload to PyPI. The second section will define the remote repository's name and type.

```{code-block} toml
[tool.semantic_release]
version_variable = "pyproject.toml:version"
commit_version_number = true
upload_to_pypi = "false"

[tool.semantic_release.remote]
name = "origin"
type = "gitlab"
```

```{code-cell} bash
:tags: [remove-input]
echo $'
[tool.semantic_release]
version_variable = "pyproject.toml:version"
commit_version_number = true
upload_to_pypi = "false"

[tool.semantic_release.remote]
name = "origin"
type = "gitlab"' >> pyproject.toml
```

## Setup Gitlab for Continuous Deployment

Now we will add a semantic-release step to our `.gitlab-ci.yml` file to automate the versioning and release process. This step will run in the `deploy` stage and will be triggered when a commit is made to the default branch that follows semantic versioning in its commit message.

Let's replace the content of the `.gitlab-ci.yml` file with the following configuration:

```{code-block} yaml
image: python:latest

before_script:
  - git checkout "$CI_COMMIT_REF_NAME"
  - pip install poetry
  - poetry install --only dev --no-root
  
semantic-release:
  stage: deploy
  rules:
    - if: '$CI_COMMIT_MESSAGE =~ /^(\d+\.)?(\d+\.)?(\d+).*/ && $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH'
      when: never
    - when: always
  script:
    - poetry run semantic-release -vvv version
    - poetry run semantic-release -vvv publish
```

We are using the `python:latest` image to run our CI/CD pipeline. We also set up the `before_script` to configure the git user and checkout the branch. The `semantic-release` job is defined to run in the `deploy` stage and is triggered when a commit is made to the default branch that follows semantic versioning in its commit message. The job will install `python-semantic-release` and run the `version` and `publish` commands. Finally, it will display the contents of the `pyproject.toml` file for verification.

```{code-cell} bash
:tags: [remove-input]
touch .gitlab-ci.yml
echo $'image: python:latest

before_script:
  - git checkout "$CI_COMMIT_REF_NAME"
  - pip install poetry
  - poetry install --only dev --no-root
  
semantic-release:
  stage: deploy
  rules:
    - if: \'$CI_COMMIT_MESSAGE =~ /^(\d+\.)?(\d+\.)?(\d+).*/ && $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH\'
      when: never
    - when: always
  script:
    - poetry run semantic-release -vvv version
    - poetry run semantic-release -vvv publish
    ' >> .gitlab-ci.yml
```

## Commit all changes

Commit all the changes to the repository, using the message "feat(semantic-release): add semantic release to the repository".

```{code-cell} bash
:tags: ["remove-input","remove-output"]
# git init --initial-branch=main
# git remote add origin git@gitlab.com:msdp.book/semver.git
git add .
git commit -m "feat(semantic-release): add python-semantic-release and gitlab-ci.yml"
git push --set-upstream origin main
```

## Make Semantic Commits

To ensure `python-semantic-release` correctly increments version numbers, use semantic commit messages (e.g., `fix:`, `feat:`, `BREAKING CHANGE:`) for your commits. This practice helps the tool to automatically determine the next version number based on the changes made.
You can find more information about semantic commits messages supported by `python-semantic-release` [here](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html).

```{admonition} What to notice
:class: hint

- After pushing our first commit and successfully running `python-semantic-release`, the tool will automatically generate both a release and a tag for your project, as well as a `CHANGELOG.md` file. You can find the generated release in the [Releases section](https://Gitlab.com/msdp.book/my-package/releases) of the `my-package` repository. This section provides detailed information about what's new, improved, or fixed in each release, along with any associated assets.

Similarly, the automatically created tag, marking the specific point in the repository's history for the release, can be found in the [Tags section](https://Gitlab.com/msdp.book/my-package/tags). Tags serve as important reference points, indicating version releases and facilitating easy navigation through the project's version history.
```

## See it in action

You can create a new commit with a semantic commit message and push it to the repository to see `python-semantic-release` in action. For example, you can create a new file in the repository and push it to the default branch.

```{code-block} bash
cd tests
touch test.py
git add test.py
git commit -m "feat(test): add new test module"
git push --set-upstream origin master
```

% Teardown
%```{code-cell} bash
%gh repo delete semver --yes
%```

## References 
[Semantic Versioning](https://semver.org/)