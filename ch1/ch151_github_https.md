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

In this section you will see how to create and manage your first remote repository with Github, including remote configuration, pushing changes, and cloning repositories.

## Creating and commiting to a remote repository on Github

### Create the remote repository
We will start by creating a remote repository on Github using a Web browser. We need to log into our Github account.

In the upper-right corner of any page, select +, then click New repository.

Use `my-project` as the repository name, and select Private. You can also add a description if you want. Do not initialize the repository with a README, .gitignore, or license, as we will do that later. 

Click Create repository.

```{code-cell} bash
:tags: ["remove-input","remove-output"]
gh repo create my-project --private
```

## Setting up your local project to push changes to a remote repository on Github

Inside the `my-project` directory, we will tell Git that we want to work with a remote repository on Github.

### Adding a remote repository to your local repository
To add a remote repository, use the `remote add <short name> <url>` command. This command adds, to your local repository, a reference to a remote repository. We will follow the convention of using `origin` as the short name of the remote repository. For the URL we will use the SSH URL of the remote repository on Github. 

For Github user `msdp.book`, and a repository named `my-project` the command to add the remote repository would be:

```{code-cell} bash
git remote add origin https://github.com/mcallara/my-project.git
```

```{admonition} Note
:class: note
 - For the URL, we used the HTTPS URL, so you will need to provide your credentials when prompted. You can also use the SSH URL of the remote repository to leverage the SSH key authentication.

Conventions:
 - We used `origin` for the remote repository reference. 
 - We used the name of the local repository (`my-project`) for the name of our remote repository. 
These are two common conventions but you can use any names you want.
```

### List the remote repository connections

Git provides the `remote` command to list the remote repositories linked to your local repository. 

```{code-cell} bash
git remote
```

With the `-v` option, you can see the URLs used for fetching and pushing data.

```{code-cell} bash
git remote -v
```

- `(fetch)`: This specifies the URL used for fetching data from the remote repository. Fetching involves downloading objects and refs from the remote repository to update your local repository's history.

- `(push)`: This indicates the URL used for pushing data to the remote repository. Pushing involves sending your local commits to the remote repository to update its history and potentially update branches on the remote.

### Inner workings: remote config
If we inspect the `.git/config` file, we can now see the configuration for the remote repository.

```{code-cell} bash
cat .git/config
```

### Checking references
Even though we configured the remote repository, we have not yet pushed any changes to it. Therefore, the `.git/refs` directory does not contain any references to the remote repository. If we look into the `.git/refs` directory to see references, we still only see `heads` and `tags`.

```{code-cell} bash
ls .git/refs
```

### Pushing to the remote repository
Push your changes to the remote repository on Github, setting `origin` as the upstream for `main`.

```{code-cell} bash
git push -u origin main
```

Now that we have pushed our changes to the remote repository, we can see the branches and commits in the remote repository. You can go to the Github website and navigate to the `my-project` repository to see the changes.

### Inner workings: remote refs
After pushing, if we inspect the `.git/refs` again we see that the `remotes` directory has been created and now contains a reference to the remote repository.

```{code-cell} bash
ls .git/refs
```

```{code-cell} bash
ls .git/refs/remotes
```

### Listing branches and commits

```{code-cell} bash
git branch --all
```

```{code-cell} bash
git log
```

```{admonition} What to notice
:class: hint
- We see a new branch `origin/main` which is a reference to the `main` branch in the remote repository.
- `origin/main` points to the same commit as `main`.
```

## Cloning a repository
Clone the `my-project` into a new directory named `my-project-remote`.

```{code-cell} bash
cd ..
git clone https://github.com/mcallara/my-project.git my-project-remote
ls
```

## Deleting a remote repository

To delete the remote repository in Github, navigate to the repository settings, scroll down to the Danger Zone section, and click on "Delete this repository". You will be prompted to confirm the deletion by typing the repository name.

```{code-cell} bash
:tags: ["remove-input","remove-output"]
gh repo delete my-project --yes
```