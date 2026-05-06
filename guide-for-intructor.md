# Chapter 1
- Students can use authentication via VS Code.

For the book, we leverage several types of authentication. Since we use Github CLI (`gh`) to create/delete repos and we use `git` to push/clone to the repos, the instructor needs to authenticate `gh`  (via `gh auth login`) and also to authenticate `git` in the Github Action runner.

All authentication is done through a Classic Token that needs the folllowing scopes:

`workflow` (to be able to update workflows in the repository)
`repo` (to be able to create and delete repositories, and to push code to the repositories. This get automatically marked with `workflow` scope)
`delete_repo` (to be able to delete repositories)
`read:org` (to be able to read organization information)

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

``` bash
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


# Chapter 4
The chapter is interactive and depends on live GitHub Copilot Chat / Agent
mode interactions. The book pages contain **representative known-good
outputs** for each prompt; if a live demo diverges from the shown output,
name the divergence as an instance of the failure mode under study and use
the printed result.

## Prerequisites for the instructor session
- A GitHub account with Copilot enabled and Agent mode available in VS Code.
- `uv` (>= 0.5) and `gh` installed. `uvx` ships with `uv` and is used to run
  the fetch MCP server in §4.2.3 — no Docker, no API token, no extra setup.
- Network access to `git-scm.com` and `docs.python.org` from the demo
  machine; the fetch MCP demo retrieves these pages live.

## Demo repository and fixtures
- The running project is `autograde`, scaffolded fresh by the student in §4.0.7.
- Two fixture Git repositories are constructed inline by shell commands at
  the top of §4.1.2 (`good_repo` and `broken_repo`). They are **not**
  committed to the book repo because nested `.git/` directories interfere
  with the book's own version control.
- The instructor maintains a reference implementation of `autograde`
  (private repo) used as the oracle in §4.2.6. Run it against both fixtures
  before class to confirm the expected PASS/FAIL list.

## Pre-class warm-up for §4.2.3 (fetch MCP demo)
The demo retrieves `https://git-scm.com/docs/git-merge-base` and
`https://git-scm.com/docs/git-rev-list` live. To avoid the first-run
download delay during class, run once before the session:

```bash
uvx mcp-server-fetch --help
```

This caches the package in `uv`'s tool directory; subsequent invocations
during class start instantly.

## Time budget per subsection
- §4.0 (`ch40.md`) — 30 min, mostly lecture.
- §4.1 (`ch41-sdd-tdd.md`) — 60 min, two hands-on loops (SDD then TDD).
- §4.2 (`ch42-artifacts.md`) — 60 min, four artifact demos plus closing run.

## Post-class artifact checklist
At the end of the class the student's `autograde` repository should contain:
- `specs/` with at least four spec files (`001` through `004`).
- `tests/test_*.py` with passing tests; `tests/fixtures/good_repo/` and
  `broken_repo/`.
- `AGENTS.md` at the repo root.
- `.github/prompts/grill-check.prompt.md`.
- A configured `mcp.servers.fetch` entry in their VS Code `settings.json`.
- A configured `chat.tools.terminal.autoApprove` entry in their VS Code
  `settings.json`.
- A working `autograde` CLI implementing checks #1–#4 at minimum, with #10
  added during the closing run in §4.2.6.


# Chapter 5
In section 5.2, the last set the conventional commits needs to be executed manually. In the book they are not active because there was no easy way to guarantee that the semantic release workflow was completed before the commit was executed, which caused the workflow to fail.

Section 5.3, it is intended to be done manually on Github in the same repository of section 5.2.