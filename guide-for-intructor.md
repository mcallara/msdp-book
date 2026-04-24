# Chapter 1
- Students can use authentication via VS Code.

For the book, we leverage several types of authentication. Since we use Github CLI (`gh`) to create/delete repos and we use `git` to push/clone to the repos, the instructor needs to authenticate `gh`  (via `gh auth login`) and also to authenticate `git` in the Github Action runner.

All authentication is done through a Classic Token that needs the folllowing scopes:

`delete_repo`, `read:org`, `repo`

# Authentication to run `gh` commands in the Github Action Runner
The instructor needs to authenticate `gh` in the Github Action runner through a Classic Token that it is stored as a secret in the jupyter book repository and it is available in the runner as an environment variable named `GH_TOKEN`.

This is done by adding the following env variable to the step that runs the `gh` commands in the Github Action workflow:
``` yaml
      - name: Build HTML Assets
        run: uv run jupyter-book build --html --execute
        env:
          GH_TOKEN: ${{ secrets.CREATE_DELETE_REPOS_TOKEN }}
```
# Authentication to run git commands in the Github Action Runner


by running the following command in the notebook 

```` bash
set -euo pipefail

# GH_TOKEN must already be present in runner env
: "${GH_TOKEN:?GH_TOKEN is required}"

# Avoid leaking secrets if xtrace is enabled elsewhere
set +x

# Configure a credential helper that serves GH_TOKEN on demand
git config --global credential.https://github.com.helper \
  '!f() { test "$1" = get || exit 0; echo "username=x-access-token"; echo "password=${GH_TOKEN}"; }; f'
```

we can then run `git` commands in the Github Action runner without any further authentication. The `git` commands will use the credential helper to get the token and authenticate to Github.