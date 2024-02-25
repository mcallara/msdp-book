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
cd my-project
```

# 1.5 Remote Repositories

In this section you will see how to create and manage your first remote repository with Gitlab, including remote configuration, pushing changes, and cloning repositories.

## Creating a remote repository in GitLab

In this section, you will set up your local project to push changes to a remote repository on GitLab.
Inside the `my-project` directory, we will tell Git that we want to work with a remote repository on GitLab. Even though we have not created the remote repository yet, we can still configure the local repository to push changes to it. If the repository does not exist, Gitlab will create the remote repository when we push the first changes.

```{code-cell} bash
git remote add origin git@gitlab.com:msdp.book/my-project.git
```

```{admonition} Note
:class: note
 - For the URL, we used the SSH URL of the remote repository to leverage the SSH key authentication. You can also use the HTTPS URL and provide your credentials when prompted.

Conventions:
 - We used `origin` for the remote repository reference. 
 - We used the name of the local repository (`my-project`) for the name of our remote repository. 
These are two common conventions but you can use any names you want.
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
Clone the `my-project` into a new directory named `my-project-remote`.

```{code-cell} bash
cd ..
git clone git@gitlab.com:msdp.book/my-project.git my-project-remote
ls
```