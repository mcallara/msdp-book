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
if [ -d ../home ]; then
  cd ../home/ch5/my-package
else
  cd /tmp/ch5/my-package
fi

```
In this chapter, we'll explore the essentials of Python packages, package registries, and how to utilize Poetry for package management. Additionally, we will delve into automating the build and publish process using the GitLab CI/CD pipeline, by continuing our work with the `poetry-demo` project.

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

A Package Registry is a storage space for packages where they can be published, shared, and managed. It allows developers to easily distribute and install packages using package management tools. The Python Package Index (PyPI) is a popular example, but organizations often use private registries for internal tools and libraries.

## Gitlab package registry

GitLab offers a built-in package registry that allows you to publish and share packages within your projects. It supports various package formats, including Maven, npm, Conan, and PyPI. In this section, we will focus on publishing Python packages to the GitLab Package Registry.

## Building and Publishing with Poetry

To publish a package to a registry, you need to create a package distribution file. This file contains the package's code, resources, and metadata, and can be installed using package management tools. In the case of Python packages this is known as the building the package. Poetry offers a command to build the package distribution files: `poetry build`.

Once the distribution files are created, you can publish the package to a registry using `poetry publish` command.

## Automating Build and Publish with GitLab CI/CD

We can automate the build and publish process using the GitLab CI/CD pipeline. This allows us to build and publish the package whenever a new version is released, without manual intervention.

To achieve this we will add a `publish` job to our deploy stage in our `.gitlab-ci.yml` file.

### Adding the Publish job

Below is the configuration for the `publish` job in the `.gitlab-ci.yml` file. This job runs in the `deploy` stage and is designed to trigger on commits to the default branch that follow semantic versioning in their commit message.

```{code-block} yaml
publish:
  stage: deploy
  rules:
    - if: '$CI_COMMIT_MESSAGE =~ /^(\d+\.)?(\d+\.)?(\d+).*/ && $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH'
      when: always 
  script:
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
    - poetry build
    - poetry config repositories.gitlab https://gitlab.com/api/v4/projects/$CI_PROJECT_ID/packages/pypi --local
    - poetry publish --repository gitlab -u $GITLAB_USER_LOGIN -p $GITLAB_TOKEN' >> .gitlab-ci.yml
```

This configuration does the following:

1. Builds the package using `poetry build`, which generates the package distribution files.
2. Configures Poetry to use the GitLab Package Registry as a repository.
3. Publishes the package to the GitLab Package Registry using `poetry publish`.

The `rules` section ensures this job only runs when the commit message indicates a new version (following semantic versioning) and the commit is made to the default branch.

### Installing packages from PyPI with `pip`

To install a package from a registry, `pip` is commonly used. For example, to install a package named `example-package` from PyPI, you would use:

```bash
pip install example-package
```

`pip` searches for the package in PyPI (or another configured registry), downloads it, and installs it in your Python environment.

You can also install a package from the GitLab Package Registry using `pip` by specifying the registry URL and your personal access token:

```bash
pip install poetry-demo --index-url https://__token__:<your_personal_token>@gitlab.com/api/v4/projects/<your_project_id>/packages/pypi/simple
```