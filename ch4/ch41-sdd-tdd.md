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

# 4.1 Practices: Spec-Driven and Test-Driven Development

In §4.0 you scaffolded the `autograde` package, ran a smoke test, and made
the first commit. You also met the chapter's central object: a list of six
checks the CLI must perform on a target Git repository.

This section applies the chapter's two foundational practices to that list.
The first half (§4.1.1) uses **Spec-Driven Development** to implement
**check #1 — `is_git_repo`**. The second half (§4.1.2) uses
**Test-Driven Development** to implement **check #2 — `main_branch_exists`**.

```{admonition} Recall before we start
:class: tip
Without scrolling back, name three of the failure modes from §4.0.4. The
demos that follow are designed to neutralise the first two of them
(misalignment and hallucination).
```

The 6-check list is the **Ubiquitous Language** of this project. Every
spec, every prompt, every commit message in this section refers to checks by
the names below. Pin this open in a side tab while you work.

| # | Check name | Behaviour |
|---|---|---|
| 1 | `is_git_repo` | The target path is a Git repository. |
| 2 | `main_branch_exists` | Branch `main` exists. |
| 3 | `feature_branch_exists` | Branch `feature` exists. |
| 4 | `main_file1_has_three_lines` | `main:file1.txt` contains exactly three lines. |
| 5 | `main_does_not_contain_file2` | `file2.txt` is absent from `main`. |
| 6 | `feature_file2_exists` | `file2.txt` exists on `feature`. |

## 4.1.1 Spec-Driven Development

Spec-Driven Development (SDD) means **state what the system should do before
asking the agent to generate it**. With agents, that habit stops a vague
prompt from turning into a large amount of plausible but misdirected code.

The shape of the loop is:

```
Specify  →  Plan  →  Tasks  →  Implement
  ↑                                 │
  └─────────── verify ──────────────┘
```

We will run it once, end to end, to implement check #1.

### Contrast: the vague prompt

Open VS Code in your `autograde` directory. Open the Copilot Chat panel
(`Ctrl+Shift+I`). Switch the dropdown to **Agent** mode. As a baseline
experiment, paste this:

```{code-block} text
Build me an autograder for a git repo.
```

The exact response will differ from session to session, but the shape is
predictable: the agent scaffolds a much larger project than you asked for,
chooses its own framework and dependency stack, and adds features such as CI
or a web UI that were never requested. That is failure mode **#1
(misalignment)** plus **#5 (over-engineering)**.

```{admonition} Reset
:class: warning
Discard everything the agent just produced. In Copilot Chat, click
**Discard all**. Run `git status`; if anything was created outside what you
bootstrapped in §4.0.7, delete it. The next step starts from a clean slate.
```

### Step 1 — Specify

The cure for misalignment is to put intent into the chat *before* asking for
code. One way to do this is to let the agent interview you.

Copy this prompt into Copilot Chat in **Ask** mode (the chat will not edit
files; it will only talk):

```{code-block} text
You are a software engineer helping me write a specification for one
function in the `autograde` package.

The function is `check_is_git_repo(repo_path: Path) -> tuple[bool, str]`.
Its job: return (True, reason) if `repo_path` is a Git repository,
otherwise (False, reason).

Before writing anything, interview me. Ask one question at a time. Cover:
behaviour on a valid repo, behaviour on a non-existent path, behaviour on
a directory that is not a Git repo, behaviour on a bare repo, error
handling, dependencies you may use.

When my answers are complete, output the spec as Markdown with the
following sections: Behaviour, Inputs, Outputs, Edge cases, Dependencies,
Examples.
```

Answer the questions as they come. The point is not to guess the "right"
answer; it is to force the design decisions out into the open. A reasonable
set of answers might be:

- Behaviour on a valid repo → return `(True, "git repository at <path>")`.
- Non-existent path → return `(False, "path does not exist: <path>")`.
- Path is a file, not a directory → `(False, "path is not a directory")`.
- Directory exists but no `.git/` and not a worktree → `(False, "not a git repository")`.
- Bare repos → out of scope for this chapter; can return `(False, ...)`.
- Errors → no exceptions escape; always return a tuple.
- Dependencies → standard library `pathlib` only; no `gitpython` for this check.

When the interview is done, save the resulting spec as
`specs/001-is-git-repo.md`. One acceptable result is:

```{code-block} markdown
# Spec 001 — `is_git_repo`

## Behaviour
Determine whether `repo_path` points at the working tree of a non-bare Git
repository.

## Inputs
- `repo_path: Path` — absolute or relative path.

## Outputs
- `tuple[bool, str]` — `(passed, reason)`.

## Edge cases
| Case | Result |
|---|---|
| Path does not exist | `(False, "path does not exist: <path>")` |
| Path exists but is a file | `(False, "path is not a directory: <path>")` |
| Directory exists, no `.git/` | `(False, "not a git repository: <path>")` |
| Directory contains `.git/` directory | `(True, "git repository at <path>")` |
| Bare repository | `(False, "bare repositories are out of scope")` |

No exception ever escapes the function.

## Dependencies
Standard library only (`pathlib`). No `gitpython`.

## Examples
- `check_is_git_repo(Path("/tmp/missing"))` → `(False, "path does not exist: /tmp/missing")`
- `check_is_git_repo(Path("/tmp/myrepo"))` (with `.git/`) → `(True, "git repository at /tmp/myrepo")`
```

```{admonition} What just happened
:class: hint
The important change is not the wording. It is that the edge cases and
constraints now exist on disk before any code is written.
```

### Step 2 — Plan and Tasks

A spec describes *what*. A plan describes *how*. Switch Copilot Chat to
**Agent** mode and paste:

```{code-block} text
Read `specs/001-is-git-repo.md`. Produce two files:

`plan.md` — one paragraph describing the implementation approach, one
paragraph on testing strategy, one paragraph on integration with the CLI.

`tasks.md` — an ordered checklist of vertical slices, each independently
committable. Use `- [ ]` checkboxes. Maximum 6 tasks.

Do not write any other code yet.
```

One acceptable `tasks.md` looks like this:

```{code-block} markdown
# Tasks for spec 001

- [ ] T1. Create `autograde/checks/__init__.py`.
- [ ] T2. Create `autograde/checks/is_git_repo.py` with the function signature only and a docstring referencing the spec.
- [ ] T3. Add `tests/test_is_git_repo.py` with one test per row of the spec's edge-case table.
- [ ] T4. Implement `check_is_git_repo` until all tests pass.
- [ ] T5. Wire the check into `autograde.main` so `autograde PATH` reports it.
- [ ] T6. Update the smoke test to invoke `autograde` against the package's own directory.
```

Review the task list before moving on. If a task is too large, split it; if a
task is missing, add it.

### Step 3 — Implement T1–T2

Now ask the agent to do the first two tasks:

```{code-block} text
Implement T1 and T2 from `tasks.md`. Stop after T2. Do not start T3 yet.
```

When the agent stops, run:

```{code-block} bash
uv run pytest
git diff
```

Read the diff. The new file should look something like:

```{code-block} python
"""Check 001: is_git_repo.

See `specs/001-is-git-repo.md` for the contract.
"""
from pathlib import Path


def check_is_git_repo(repo_path: Path) -> tuple[bool, str]:
    """Return (passed, reason) for the is_git_repo check.

    Not yet implemented; see tasks.md T4.
    """
    raise NotImplementedError
```

If the diff matches the spec, accept it and commit:

```{code-block} bash
git add .
git commit -m "spec 001: scaffold check_is_git_repo (T1, T2)"
```

### Reflection

Before writing the implementation, you have already done four valuable things:

1. Forced yourself to articulate intent (the interview).
2. Committed that intent to disk (`specs/001-is-git-repo.md`).
3. Decomposed the work into reviewable slices (`tasks.md`).
4. Reviewed the agent's first concrete change before accepting it.

```{admonition} Failure modes neutralised
:class: note
- **#1 misalignment** — the spec exists *before* the code; the agent has nowhere to drift to.
- **#2 hallucination** — the spec restricts dependencies to the standard library; the agent cannot invent imports.
- **#5 over-engineering** — the task list bounds the work; the agent stops at T2.
```

We stop SDD here, with the function stubbed and the contract written. T3 — the
test — is the natural starting point for the next loop.

## 4.1.2 Test-Driven Development with the agent

**Test-Driven Development** (TDD) writes the test for a behaviour *before*
the code that implements it. Kent Beck described the loop in *Test-Driven
Development: By Example* (2002) as:

```
Red  →  Green  →  Refactor
```

- **Red.** Write a small test for the next slice of behaviour. Run it. It
  fails — usually because the function it calls does not yet exist. The
  test bar goes red.
- **Green.** Write the smallest amount of code that makes that test pass.
  Nothing more. Run the suite again; the bar goes green.
- **Refactor.** With a green bar as a safety net, improve the structure of
  the code (rename, extract, deduplicate) without changing what it does.
  Re-run the suite after each change to confirm the bar stays green.

The discipline feels backwards at first, but it buys two things: each new
piece of production code starts life with a test that pins its behaviour, and
you always have a fast answer to *"did the last change break anything?"*

Kent Beck argued in 2025 that "**TDD becomes more valuable when code
generation is cheap**." If code is cheap, tests become the main thing that
keeps the code aligned with the intended behaviour.

There is, however, a trap.

### Contrast: the TDD prompting paradox

A March 2026 paper, *TDD Anti-Patterns in Agentic Development*
(arXiv 2603.17973), showed that a vague instruction to "use TDD" can be worse
than no TDD instruction at all. Agents tend to add excessive mocking, pin the
implementation instead of the behaviour, and refactor themselves into brittle
designs.

Compare these two prompts:

```{code-block} text
# Bad — vague TDD instruction
Add the next check using TDD.
```

```{code-block} text
# Good — targeted TDD instruction
A failing test exists at `tests/test_main_branch_exists.py`. It uses the
fixture repos in `tests/fixtures/good_repo/` and `tests/fixtures/broken_repo/`.

Make this test pass without modifying the test file. Follow the same
implementation pattern as `autograde/checks/is_git_repo.py`. After the test
goes green, run the entire test suite and report the result.
```

The good version names the test, the fixtures, the pattern to follow, and the
success criterion. That removes the space where the agent would otherwise be
creative in the wrong direction.

```{admonition} The pedagogical contract for TDD with agents
:class: important
**You write the test. The agent writes the implementation.** Reversing this
is a common way the loop fails.
```

### Step 1 — Red: a shipped failing test

For check #2 we provide the test so the exercise stays focused on the loop,
not on designing fixtures from scratch. First create the fixture repositories.
From the root of your `autograde` project:

```{code-block} bash
mkdir -p tests/fixtures
cd tests/fixtures

git init -q good_repo
cd good_repo
git checkout -q -b main
echo -e "line1\nline2\nline3" > file1.txt
git add file1.txt
git -c user.email=you@example.com -c user.name=you commit -q -m "Add file1"
cd ..

git init -q broken_repo
cd broken_repo
# Note: deliberately do NOT create a `main` branch.
git checkout -q -b master
echo "anything" > file1.txt
git add file1.txt
git -c user.email=you@example.com -c user.name=you commit -q -m "Initial"
cd ../../..
```

Now create `tests/test_main_branch_exists.py` exactly as shown:

```{code-block} python
# tests/test_main_branch_exists.py
from pathlib import Path

import pytest

from autograde.checks.main_branch_exists import check_main_branch_exists

FIXTURES = Path(__file__).parent / "fixtures"


def test_good_repo_has_main():
    passed, reason = check_main_branch_exists(FIXTURES / "good_repo")
    assert passed is True
    assert "main" in reason


def test_broken_repo_lacks_main():
    passed, reason = check_main_branch_exists(FIXTURES / "broken_repo")
    assert passed is False
    assert "main" in reason


def test_missing_path_returns_false():
    passed, reason = check_main_branch_exists(Path("/nonexistent/path/xyz"))
    assert passed is False


def test_returns_tuple_of_correct_types():
    result = check_main_branch_exists(FIXTURES / "good_repo")
    assert isinstance(result, tuple)
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)
```

Run the suite to confirm the test is **red** for the right reason:

```{code-block} bash
uv run pytest tests/test_main_branch_exists.py
```

You should see an `ImportError` because the module
`autograde.checks.main_branch_exists` does not exist yet. That is the right
red state: the implementation is missing, and the test is doing useful work.

### Step 2 — Green: the agent implements

Now use a targeted prompt. In Copilot Chat (Agent mode):

```{code-block} text
A failing test exists at `tests/test_main_branch_exists.py`. It uses the
fixture repos in `tests/fixtures/good_repo/` and `tests/fixtures/broken_repo/`.

Make this test pass without modifying the test file. Follow the same
implementation pattern as `autograde/checks/is_git_repo.py`: standard
library only, signature `check_main_branch_exists(repo_path: Path) ->
tuple[bool, str]`, no exceptions escape. After the test goes green, run
the entire test suite and report the result.
```

A representative known-good implementation:

```{code-block} python
# autograde/checks/main_branch_exists.py
"""Check 002: main_branch_exists."""
from pathlib import Path


def check_main_branch_exists(repo_path: Path) -> tuple[bool, str]:
    """Return (True, reason) if the repository at `repo_path` has a `main` branch."""
    if not repo_path.exists():
        return False, f"path does not exist: {repo_path}"
    head_ref = repo_path / ".git" / "refs" / "heads" / "main"
    packed = repo_path / ".git" / "packed-refs"
    if head_ref.exists():
        return True, "main branch found in refs/heads/main"
    if packed.exists() and "refs/heads/main" in packed.read_text():
        return True, "main branch found in packed-refs"
    return False, f"no main branch in {repo_path}"
```

Watch the output stream. The agent should:

1. Open the existing `is_git_repo.py` to learn the pattern.
2. Open the failing test to learn the fixture paths and assertions.
3. Create `autograde/checks/main_branch_exists.py`.
4. Run pytest in the integrated terminal.
5. Iterate if anything fails.

When the agent reports success, **verify it yourself**:

```{code-block} bash
uv run pytest
```

All four tests should pass. If they do not, read the failure and decide
whether the test is wrong or the implementation is wrong before asking the
agent to try again. Tie-breaking is a human job.

### Step 3 — Refactor

The first green implementation is rarely the final one. With the tests as a
safety net, ask the agent to improve readability:

```{code-block} text
Both `is_git_repo.py` and `main_branch_exists.py` open the repository
directory. Extract a private helper `_open_repo(path: Path) -> Path | None`
that returns the repo path if it is a non-bare git repository or `None`
otherwise. Refactor both checks to use it. Run the test suite after each
file change. Do not modify any tests.
```

Review the resulting diff. The `_open_repo` helper should appear in a new
file such as `autograde/checks/_repo.py`, and the two existing checks should
become slightly shorter without changing behaviour.

Commit the work as three separate commits — one per file change, in the
order the agent made them — so future you (or your reviewer) can read the
refactor as a story:

```{code-block} bash
git add autograde/checks/main_branch_exists.py tests/test_main_branch_exists.py tests/fixtures
git commit -m "spec 002: implement check_main_branch_exists (red → green)"

git add autograde/checks/_repo.py
git commit -m "refactor: extract _open_repo helper"

git add autograde/checks/is_git_repo.py
git commit -m "refactor: use _open_repo in is_git_repo"
```

### Reflection

```{admonition} Failure modes neutralised
:class: note
- **#2 hallucination** — the test pinned the behaviour; an invented API would have failed the assertion.
- **#5 over-engineering** — the test bounded the scope; the agent could not add a CLI framework or a dashboard.
- **#6 codebase entropy** — the refactor with the test suite as a net let us improve the design without breaking anything.
```

```{admonition} The takeaway from this section
:class: tip
The TDD prompting paradox is a common way teams new to
agentic TDD fail. The fix is not to abandon TDD — it is to make the
instruction *targeted*: name the test, the fixtures, the existing pattern,
and the success criterion in the prompt itself.
```

You now have **two of six checks implemented**, a `specs/` folder, a
`tasks.md`, two fixture repositories, and a clean test suite. More
importantly, you have a workflow that already works.

In §4.2 we will harden it.

```{admonition} References
:class: seealso
- *Spec-Driven Development* — GitHub Blog, September 2025; *Spec Kit* open source release.
- *Test-Driven Development with AI* — Kent Beck, 2025.
- *TDAD: TDD Anti-Patterns in Agentic Development* — arXiv 2603.17973, March 2026.
- *Building Effective Agents* — Anthropic Engineering, 2024.
```
