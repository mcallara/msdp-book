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
% Create Gitlab account
% In this section, we will learn to use Poetry to build and publish our Python package in the Gitlab Package Registry. 
% We will use the Gitlab CI/CD pipeline to automate the build and publish process.
% We will continue our work with the `poetry-demo` project. Since, in the previous section, we added a GITLAB_TOKEN variable to our repo, you don't need to do it again.

# 5.3 Packaging
```{code-cell} bash
:tags: [remove-input]
cd ../home/ch55/poetry-demo
```
In this chapter, we'll explore the essentials of Python packages, package registries, and how to utilize Poetry for package management. Additionally, we will delve into automating the build and publish process using the GitLab CI/CD pipeline, building on our work with the `poetry-demo` project.

## Understanding Python Packages and Package Registries

A **Python Package** is a collection of modules that are bundled together. These packages can be easily distributed for use in other projects, promoting code reuse and modular programming. Python packages can include libraries, frameworks, or collections of code and resources for specific purposes.

A **Package Registry** is a storage space for packages where they can be published, shared, and managed. It allows developers to easily distribute and install packages using package management tools. The Python Package Index (PyPI) is a popular example, but organizations often use private registries for internal tools and libraries.

### Using a Package Registry with `pip`

To install a package from a registry, `pip` is commonly used. For example, to install a package named `example-package`, you would use:

```bash
pip install example-package
```

`pip` searches for the package in PyPI (or another configured registry), downloads it, and installs it in your Python environment.

## Building and Publishing with Poetry

[Poetry](https://python-poetry.org/) is a modern tool for Python package management and dependency resolution. It simplifies package creation, dependency management, and packaging.

### Publishing to GitLab Package Registry

To publish our package to the GitLab Package Registry, we'll first ensure our project is configured to use Poetry. Then, we'll set up our `.gitlab-ci.yml` to automate the build and publish process.

### Pre-requisites

- A GitLab repository with our Python project (`poetry-demo`).
- A `pyproject.toml` file configured for our project, created by running `poetry init`.
- The `GITLAB_TOKEN` variable already added to our GitLab project settings for authentication.

## Automating Build and Publish with GitLab CI/CD

GitLab CI/CD pipelines automate steps in the software delivery process, such as builds, tests, and deployments. We'll add a `publish` stage to our `.gitlab-ci.yml` to automate publishing our package to the GitLab Package Registry whenever a new version is tagged.

### Adding the Publish Stage

Below is the configuration for the `publish` stage in the `.gitlab-ci.yml` file. This stage runs in the `deploy` phase and is designed to trigger on commits to the default branch that follow semantic versioning in their commit message.

```{code-block} yaml
publish:
  stage: deploy
  rules:
    - if: '$CI_COMMIT_MESSAGE =~ /^(\d+\.)?(\d+\.)?(\d+).*/ && $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH'
      when: always 
  script:
    - pip install poetry
    - poetry build
    - poetry config repositories.gitlab https://gitlab.com/api/v4/projects/$CI_PROJECT_ID/packages/pypi --local
    - poetry publish --repository gitlab -u $GITLAB_USER_LOGIN -p $GITLAB_TOKEN
```

```{code-cell} bash
:tags: [remove-input]
echo $'
publish:
  stage: deploy
  rules:
    - if: \'$CI_COMMIT_MESSAGE =~ /^(\d+\.)?(\d+\.)?(\d+).*/ && $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH\'
      when: always 
  script:
    - pip install poetry
    - poetry build
    - poetry config repositories.gitlab https://gitlab.com/api/v4/projects/$CI_PROJECT_ID/packages/pypi --local
    - poetry publish --repository gitlab -u $GITLAB_USER_LOGIN -p $GITLAB_TOKEN' >> .gitlab-ci.yml
```

This configuration does the following:

1. Installs Poetry if it's not already available in the CI/CD environment.
2. Builds the package using `poetry build`, which generates the package distribution files.
3. Configures Poetry to use the GitLab Package Registry as a repository.
4. Publishes the package to the GitLab Package Registry using `poetry publish`.

The `rules` section ensures this job only runs when the commit message indicates a new version (following semantic versioning) and the commit is made to the default branch.