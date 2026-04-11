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
cd ../home
mkdir -p ch1
cd ch1
```

# 1.1 Your First Steps with the Command Line

Before jumping into the world of Git, you first need to be comfortable with the command line. This section will introduce you to the basic commands that are essential for navigating your computer and managing files. Think of it as learning the alphabet before you start writing sentences.

## The Command Line Interface

The command line is a powerful, text-based tool for interacting with your computer. It allows you to perform tasks, manage files, and run programs by typing commands instead of clicking on icons.

### The Prompt

When you open the command line, you are greeted by the **prompt**. It typically shows information like your username, the machine's name (hostname), and your current location (directory). For example:

```
user@hostname:~$
```

Let's break this down:

*   `user`: The current logged-in user.
*   `hostname`: The name of the computer.
*   `~`: A shortcut for your home directory.
*   `$`: A standard symbol indicating you are logged in as a regular user. An administrator (or root) user often sees a `#` symbol.

## Where Am I? Finding Your Place

The first thing you need to know is how to find out where you are in the file system.

To display the full path of your current directory, use the `pwd` (print working directory) command:

```{code-cell} bash
pwd
```

This command will print the absolute path from the root of the file system (`/`) to your current location.

Now that you know where you are, let's see what's in there. To list the files and directories in your current location, use the `ls` (list) command:

```{code-cell} bash
ls
```

## Navigating the File System

Knowing where you are is useful, but you'll often need to move around. The `cd` (change directory) command is your tool for navigation.

First, let's create a new directory to practice with. To create a directory, use the `mkdir` (make directory) command:

```{code-cell} bash
mkdir my-test-folder
```

Now, to move into your new `my-test-folder` directory, use `cd` followed by the directory name:

```{code-cell} bash
cd my-test-folder
```

```{admonition} What to notice
:class: hint
Look at your prompt! It has likely changed to show that you are now inside the `my-test-folder` directory. For example: `user@hostname:~/my-test-folder$`. This is a helpful, constant reminder of your current location.
```

You can confirm your new location with `pwd`:

```{code-cell} bash
pwd
```

To go back up one level to the parent directory, you can use the special `..` argument:

```{code-cell} bash
cd ..
```

```{admonition} Test your knowledge
:class: seealso
Practice makes perfect. Try these steps:
1. Create a new directory called `practice`.
2. Navigate into the `practice` directory.
3. Use `pwd` to confirm you are inside `practice`.
4. Navigate back to the parent directory.
```

## Creating and Managing Files

Now that you can navigate, let's create and work with files.

To create a new, empty file, use the `touch` command:

```{code-cell} bash
touch notes.txt
```

To add content to a file, you can use the `echo` command combined with the `>` redirection operator.

```{code-cell} bash
echo "Hello, Command Line!" > notes.txt
```

```{admonition} Behind the scenes: Redirection
:class: tip
The `>` symbol is a **redirection operator**. It takes the output of the command on its left (in this case, the text "Hello, Command Line!") and, instead of printing it to the screen, writes it into the file on its right (`notes.txt`). Be careful: if the file already has content, `>` will overwrite it completely. To append content, use `>>`.
```

To display the content of your new file, use the `cat` (concatenate) command:

```{code-cell} bash
cat notes.txt
```

## Cleaning Up Your Workspace

To keep things tidy, you'll need to know how to delete files and directories.

To remove a file, use the `rm` (remove) command:

```{code-cell} bash
rm notes.txt
```

To remove an empty directory, you can use `rmdir`. However, to remove a directory and all the files and subdirectories inside it, you need to use `rm` with the `-r` (recursive) option.

Let's remove the `my-test-folder` directory we created earlier:

```{code-cell} bash
rm -r my-test-folder
```

```{admonition} Danger: rm is forever
:class: danger
The `rm` command is powerful and irreversible. There is no "Recycle Bin" or "Trash" on the command line. Once a file is deleted with `rm`, it's gone for good. Always double-check which directory you are in (`pwd`) and what you are deleting before you press Enter. You can add the `-i` (interactive) flag to prompt for confirmation before each removal.
```

## Getting Help

Almost every command has a help page that lists its options and how to use them. To see it, you can usually use the `--help` flag.

```{code-cell} bash
:tags: [scroll-output]
ls --help
```

## Introduction to Git

Now that you have a handle on the basic command-line tools, you're ready to start with Git. Git is a version control system that runs on the command line, which is why we started there.

First, let's check if Git is installed and what version you have.

```{code-cell} bash
:tags: [scroll-output]
git --version
```

If this command returns a version number (e.g., `git version 2.34.1`), you're ready to go. If you get an error, you'll need to install Git first.

## Configuring Git

The first thing you should do after installing Git is to tell it who you are. This information is attached to every change you make, so it's important for collaboration.

To set your username and email address for all your projects (globally), use the `git config` command:

```{code-cell} bash
git config --global user.name "msdp-book"
git config --global user.email "msdp.book@gmail.com"
```

To check your settings, you can list the global configuration:

```{code-cell} bash
git config --global --list
```

```{admonition} Know more: System vs Global vs Local Configuration
:class: note
Git uses three levels of configuration:
*   `--system`: Settings for every user on the computer.
*   `--global`: Settings for you, the current user, across all your projects.
*   `--local`: Settings for the specific project (repository) you are currently in. This is the default if you don't specify a level.
Local settings override global settings, which in turn override system settings.
```