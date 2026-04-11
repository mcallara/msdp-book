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

```{code-cell} bash
:tags: ["remove-input","remove-output"]
cd ../home/ch4/my-package
```

# 4.3 Dependency Management and Virtual Environments

## Dependency Management

Managing dependencies is an important aspect of our software development process. Poetry simplifies this task through an intuitive set of commands and a modern `pyproject.toml` file structure that follows Python standards.

### Understanding Modern Poetry Project Structure

Poetry 2.1+ supports the standard PEP 621 `project` section alongside the traditional `tool.poetry` section. The modern approach is to use the `project` section for metadata and dependencies that are standard across Python packaging tools, while using `tool.poetry` for Poetry-specific configurations.

### Adding Dependencies
To see how we declare dependencies in a Poetry project. Let's first add a simple module to our `my-package` project to simulate a common use case. To do so, let's create a new file called `analysis.py` in the `my-package/src/my-package` directory with the following content: 

```{code-block} python
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
```

```{code-cell} bash
:tags: ["remove-input","remove-output"]
cd src
cd my_package
echo $'import pandas as pd
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})' > analysis.py
cd ..
cd ..
```

Pandas is a popular library for data manipulation and analysis in Python very frequently used in Data Science projects. 

Now we want to use Poetry to keep track that our project requires `pandas` as a dependency. To add `pandas` as a dependency, run the following command in your project directory:

```{code-cell} bash
:tags: ["remove-input","remove-output"]
conda activate py3.12_clean
poetry add pandas
```

```{code-block} bash
poetry add pandas
```

```{admonition} What to notice
:class: hint 
- Modern Poetry projects use the standard `project` section for dependencies when possible
- If the project was setup with python 3.8, Poetry will not add `pandas` as a dependency and let us know that pandas requires python 3.9 or higher.
```

We can update the `pyproject.toml` file to use Python 3.9 or higher. The structure looks like this:

```{code-block} toml
[project]
name = "my-package"
version = "0.1.0"
description = ""
authors = [
    {name = "msdp-book",email = "msdp.book@gmail.com"}
]
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pandas (>=2.3.1,<3.0.0)"
]

[tool.poetry]
packages = [{include = "my_package", from = "src"}]


[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

```{admonition} What to notice
:class: hint 
- We see that `pandas` was added as a dependency in the `project.dependencies` array.
- We also see that a `poetry.lock` file was created.
- Dependencies are now managed in the standard `project` section following PEP 621.
```

### Working with Dependency Groups

Poetry 2.1+ uses dependency groups to organize different types of dependencies. For development dependencies, testing tools, documentation, etc., use dependency groups:

```{code-cell} bash
poetry add pytest --group dev
```

### Understanding Dependency Groups and Version Constraints

Modern Poetry projects organize dependencies using groups. The main dependencies go in the `project.dependencies` section, while development and other specialized dependencies are organized in groups under the `tool.poetry.group.<group_name>.dependencies` sections.

Let's look at the updated `pyproject.toml` structure after adding our dependencies:

```{code-block} toml
[project]
name = "my-package"
version = "0.1.0"
description = ""
authors = [
    {name = "msdp-book",email = "msdp.book@gmail.com"}
]
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pandas (>=2.3.1,<3.0.0)"
]

[tool.poetry]
packages = [{include = "my_package", from = "src"}]


[tool.poetry.group.dev.dependencies]
pytest = "^8.4.1"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

Poetry keeps track of the dependencies with version constraints to ensure compatibility and stability. The `pandas` version is specified as `>=2.0.0,<3.0.0`, which means any version of pandas 2.x is acceptable. The `^8.4.1` notation for pytest means versions `>=8.4.1,<9.0.0`.

## Virtual Environment Management with Poetry

Poetry creates and manages virtual environments automatically. If we want to run our package, we need to install it in a virtual environment along with the dependencies that we defined. Poetry makes this process seamless and handles virtual environment creation automatically.

### Configuring Poetry Virtual Environment Location

By default, Poetry stores virtual environments in a system cache directory. However, you can configure Poetry to create the virtual environment within your project's directory by setting the `virtualenvs.in-project` configuration to `true`:

```{code-block} bash
poetry config virtualenvs.in-project true
```

This configuration makes it easier to manage project environments, especially when working with version control systems or when you need to share the project with others.

### Creating and Using Your Virtual Environment

Poetry 2.1+ creates virtual environments automatically when you run `poetry install`. Unlike previous versions, you don't need to manually create environments in most cases. However, if you need to specify a particular Python version, you can still do so.

First, let's check what Python versions are available and create our virtual environment:

If you need to specify a particular Python version, you can use the `poetry env use` command. For example, if you have a clean conda environment:

```{code-block} bash
poetry env use /path/to/your/python/executable
```

Or if you have the python executable in your PATH:

```{code-block} bash
poetry env use python3.10
```

Now, let's install the dependencies in the virtual environment:

```{code-block} bash
conda deactivate
poetry install
```

We used `conda deactivate` to ensure that we are not in any other virtual environment. Otherwise, Poetry will use the currently active environment instead of creating a new one.


```{admonition} What to notice
:class: hint
- Poetry automatically creates a virtual environment if one doesn't exist
- Dependencies are installed according to the `poetry.lock` file for reproducible builds
- Both main dependencies and development group dependencies are installed by default
```

### Installing Specific Dependency Groups

Poetry 2.1+ provides fine-grained control over which dependency groups to install:

```{code-block} bash
# Install only main dependencies (no development groups)
poetry install --only main

# Install main dependencies plus specific groups
poetry install --with docs,test

# Install only specific groups (excluding main dependencies)
poetry install --only dev

# Exclude specific groups
poetry install --without test,docs
```

### Running Commands Within the Virtual Environment

If you need to run a single command within the context of your virtual environment without activating it, you can use `poetry run`. For example, to run a Python script:

```{code-block} bash
poetry run python my_package/analysis.py
```

### Activating the Virtual Environment

In Poetry 2.1+, the activation method has been updated. The `poetry shell` command has been moved to a plugin. Instead, use the `poetry env activate` command:

```{code-block} bash
# Get the activation command (you need to run the output)
poetry env activate

# Or use eval to activate directly in your current shell
eval $(poetry env activate)
```

The `poetry env activate` command prints the activate command that you can run manually or pipe to `eval` to activate the environment in your current shell.


### Managing Multiple Virtual Environments

Poetry allows you to manage multiple virtual environments for different Python versions. Here are the essential commands:

```{code-block} bash
# Display current environment information
poetry env info

# List all environments for this project
poetry env list

# Remove a specific environment
poetry env remove python3.10
poetry env remove /path/to/python/executable

# Remove all environments for this project
poetry env remove --all
```

### Understanding Dependency Resolution and Lock Files

#### The `poetry.lock` File

The `poetry.lock` file is crucial for reproducible builds:

- **With `poetry.lock`**: Ensures exact versions are installed, as specified in the lock file. Critical for reproducibility across environments.
- **Without `poetry.lock`**: Poetry resolves dependencies from `pyproject.toml` constraints and generates a new lock file.

### Version Control Best Practices

Always commit the `poetry.lock` file to version control. This ensures that all developers and deployment environments use identical dependency versions, preventing "works on my machine" issues.

### Updating Dependencies

```{code-block} bash
# Update all dependencies to their latest compatible versions
poetry update

# Update specific dependencies
poetry update pandas pytest

# Update dependencies in specific groups
poetry update --only dev
```

### Installing Dependencies Without the Project Package

```{code-block} bash
# Install dependencies without installing the project package itself
poetry install --no-root

# Use non-package mode (set in pyproject.toml)
# [tool.poetry]
# package-mode = false
```

For CI/CD environments, `--no-root` is particularly useful when you need dependencies for testing or building but not the project package itself.


## Resources and Further Reading

- Official Poetry 2.1 Documentation: [python-poetry.org/docs](https://python-poetry.org/docs/)
- Managing Dependencies: [Managing Dependencies](https://python-poetry.org/docs/managing-dependencies/)
- Managing Virtual Environments: [Managing Environments](https://python-poetry.org/docs/managing-environments/)
- The pyproject.toml file: [Pyproject Configuration](https://python-poetry.org/docs/pyproject/)
- PEP 621 (Project Metadata): [peps.python.org/pep-0621](https://peps.python.org/pep-0621/)
