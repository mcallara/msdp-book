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

## Creating a remote repository in GitLab
In this section, you will set up your local project to push changes to a remote repository on GitLab.
Inside the `my-project` directory, we will tell Git that we want to work with a remote repository on GitLab. Even though we have not created the remote repository yet, we can still configure the local repository to push changes to it. If the repository does not exist, Gitlab will create the remote repository when we push the first changes.

```{code-cell} bash
cd my-project
git remote add origin git@gitlab.com:yourusername/my-project-remote.git
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
Push your changes to the remote repository on GitLab, setting `origin` as the upstream for `main`.

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
git clone git@gitlab.com:yourusername/my-project-remote.git my-project-remote-2
ls
```

This chapter guides you through creating and managing your first GitLab repository, including remote configuration, pushing changes, and cloning repositories.
