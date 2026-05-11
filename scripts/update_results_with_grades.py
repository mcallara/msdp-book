#!/usr/bin/env python3

import argparse
import csv
import re
import subprocess
from pathlib import Path


NOTE_PATTERN = re.compile(r"^Current note:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


def read_results(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("results CSV is empty")
        return list(reader)


def write_results(csv_path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_current_note(output: str) -> str:
    match = NOTE_PATTERN.search(output)
    return match.group(1).strip() if match else ""


def run_autograder(
    autograder_dir: Path,
    tests_path: str,
    project_path: Path,
    max_score: int,
) -> tuple[str, int]:
    command = [
        "uv",
        "run",
        "autograder",
        tests_path,
        str(project_path),
        "--max-score",
        str(max_score),
    ]
    result = subprocess.run(
        command,
        cwd=autograder_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    output = result.stdout
    if result.stderr:
        output = f"{output}\n{result.stderr}" if output else result.stderr
    return output, result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the autograder for each downloaded project in a results CSV and record the current note."
    )
    parser.add_argument("results_csv", help="CSV file with at least Github user and Downloaded columns.")
    parser.add_argument(
        "--autograder-dir",
        default=".",
        help="Directory where `uv run autograder` should be executed (default: current directory).",
    )
    parser.add_argument(
        "--tests-path",
        default="tests_assignment_1",
        help="Autograder tests path passed to the autograder command (default: %(default)s).",
    )
    parser.add_argument(
        "--projects-dir",
        help="Directory containing project folders. Defaults to the directory of the results CSV.",
    )
    parser.add_argument(
        "--repo-prefix",
        default="my-project-",
        help="Folder prefix before the GitHub username (default: %(default)s).",
    )
    parser.add_argument(
        "--max-score",
        type=int,
        default=100,
        help="Maximum score passed to the autograder (default: %(default)s).",
    )
    args = parser.parse_args()

    results_csv = Path(args.results_csv).expanduser().resolve()
    autograder_dir = Path(args.autograder_dir).expanduser().resolve()
    projects_dir = (
        Path(args.projects_dir).expanduser().resolve()
        if args.projects_dir
        else results_csv.parent
    )

    rows = read_results(results_csv)
    fieldnames = list(rows[0].keys()) if rows else ["Github user", "Downloaded"]
    if "Current Note" not in fieldnames:
        fieldnames.append("Current Note")

    for row in rows:
        user = (row.get("Github user") or "").strip()
        downloaded = (row.get("Downloaded") or "").strip().lower()

        if not user:
            row["Current Note"] = ""
            continue

        if downloaded != "yes":
            row["Current Note"] = ""
            print(f"skip {user}: Downloaded is not Yes")
            continue

        project_path = projects_dir / f"{args.repo_prefix}{user}"
        if not project_path.exists():
            row["Current Note"] = ""
            print(f"missing project {user}: {project_path}")
            continue

        print(f"grade {user}: {project_path}")
        output, returncode = run_autograder(
            autograder_dir=autograder_dir,
            tests_path=args.tests_path,
            project_path=project_path,
            max_score=args.max_score,
        )
        note = parse_current_note(output)
        row["Current Note"] = note
        if note:
            print(f"note {user}: {note}")
        else:
            print(f"note {user}: not found (exit code {returncode})")

    write_results(results_csv, rows, fieldnames)
    print(f"updated results: {results_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())