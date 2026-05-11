#!/usr/bin/env python3

import argparse
import csv
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def repo_exists(user: str, repo: str) -> bool:
    url = f"https://github.com/{user}/{repo}.git"
    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", url, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def clone_repo(user: str, repo: str, output_dir: Path) -> bool:
    target = output_dir / f"{repo}-{user}"
    if target.exists():
        print(f"skip {user}: {target} already exists")
        return True

    url = f"https://github.com/{user}/{repo}.git"
    print(f"clone {user}: {url} -> {target}")
    subprocess.run(["git", "clone", url, str(target)], check=True)
    return True


def iter_users(source):
    for line in source:
        user = line.strip()
        if not user or user.lower() == "usuario github":
            continue
        yield user


def iter_users_from_csv(csv_path: Path, column: str | None):
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return

        normalized = {name.strip().lower(): name for name in reader.fieldnames}
        selected_column = column
        if selected_column is None:
            for candidate in ("usuario github", "github", "github username", "username"):
                if candidate in normalized:
                    selected_column = normalized[candidate]
                    break
            if selected_column is None:
                selected_column = reader.fieldnames[0]
        else:
            selected_column = normalized.get(selected_column.strip().lower(), selected_column)

        if selected_column not in reader.fieldnames:
            choices = ", ".join(reader.fieldnames)
            raise ValueError(f"column '{selected_column}' not found in CSV. Available columns: {choices}")

        for row in reader:
            user = (row.get(selected_column) or "").strip()
            if user:
                yield user


def resolve_csv_path(raw_path: str) -> Path:
    csv_path = Path(raw_path).expanduser()
    if csv_path.exists():
        return csv_path

    if not csv_path.is_absolute():
        candidate = SCRIPT_DIR / csv_path
        if candidate.exists():
            return candidate

    raise FileNotFoundError(f"CSV file not found: {raw_path}")


def write_results_csv(results_csv_path: Path, rows: list[dict[str, str]]) -> None:
    with results_csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Github user", "Downloaded"])
        writer.writeheader()
        writer.writerows(rows)


def resolve_output_dir(raw_output_dir: str, output_subdir: str | None, use_tmp_dir: bool) -> Path:
    if output_subdir:
        return (Path.cwd() / output_subdir).resolve()

    if use_tmp_dir:
        return (Path.cwd() / "tmp").resolve()

    return Path(raw_output_dir).expanduser().resolve()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clone a public GitHub repo for each listed user if it exists."
    )
    parser.add_argument(
        "users",
        nargs="*",
        help="GitHub usernames. If omitted, usernames are read from --csv or stdin.",
    )
    parser.add_argument(
        "--csv",
        dest="csv_path",
        help="CSV file containing GitHub usernames.",
    )
    parser.add_argument(
        "--csv-column",
        help="CSV column name that contains the GitHub username.",
    )
    parser.add_argument(
        "--repo",
        default="my-project",
        help="Repository name to look for (default: %(default)s).",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Where cloned repositories should be created (default: current directory).",
    )
    parser.add_argument(
        "--tmp-dir",
        action="store_true",
        help="Clone repositories into a tmp directory under the current working directory.",
    )
    parser.add_argument(
        "--output-subdir",
        help="Clone repositories into this subdirectory under the current working directory.",
    )
    parser.add_argument(
        "--results-csv",
        default="download_results.csv",
        help="Where to write the CSV summary (default: %(default)s).",
    )
    args = parser.parse_args()

    if args.users:
        users = args.users
    elif args.csv_path:
        try:
            users = list(iter_users_from_csv(resolve_csv_path(args.csv_path), args.csv_column))
        except FileNotFoundError as error:
            parser.error(str(error))
        except ValueError as error:
            parser.error(str(error))
    else:
        users = list(iter_users(sys.stdin))

    if not users:
        parser.error("provide usernames as arguments, via --csv, or via stdin")

    output_dir = resolve_output_dir(args.output_dir, args.output_subdir, args.tmp_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results_csv_path = Path(args.results_csv).expanduser().resolve()
    results_csv_path.parent.mkdir(parents=True, exist_ok=True)

    results = []

    for user in users:
        if repo_exists(user, args.repo):
            downloaded = "Yes" if clone_repo(user, args.repo, output_dir) else "No"
        else:
            print(f"missing {user}: https://github.com/{user}/{args.repo}")
            downloaded = "No"

        results.append({"Github user": user, "Downloaded": downloaded})

    write_results_csv(results_csv_path, results)
    print(f"wrote results: {results_csv_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())