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
:tags: [remove-input]
cd ../home/ch1
```

# 1.5 Remote Repositories

## Create your first repo
Follow the guide on GitHub's official documentation to create your first repository. Refer to [GitHub's Quickstart for Repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories).

## Exercise: Create a new empty repo on GitHub named `test-repo`
Using the URL `git@github.com:mcallara/test-repo.git`, set up your project for version control.

```{code-cell} bash
cd my-project
git remote add origin git@github.com:mcallara/test-repo.git
```

### List the remote repository connections
```{code-cell} bash
git remote
git remote -v
```

### Exploring the Git configuration
Inspect the `.git/config` file to see the remote repository configuration.

```{code-cell} bash
cat .git/config
```

### Checking references
Look into the `.git/refs` directory to see references such as heads and tags.

```{code-cell} bash
ls .git/refs
```

### Pushing to the remote repository
Push your changes to the remote repository on GitHub, setting `origin` as the upstream for `main`.

```{code-cell} bash
git push -u origin main
```

After pushing, inspect the `.git/refs` again to verify the update.

```{code-cell} bash
ls .git/refs
```

### Listing branches and commits
```{code-cell} bash
git branch --all
git log
```

```{admonition} What to notice
:class: hint
`origin/main` should be pointing to the same commit as `main`.
```

## Cloning a repository
Clone the `test-repo` into a new directory named `test-repo-2`.

```{code-cell} bash
cd ..
git clone git@github.com:mcallara/test-repo.git test-repo-2
ls
```

This chapter guides you through creating and managing your first GitHub repository, including remote configuration, pushing changes, and cloning repositories.