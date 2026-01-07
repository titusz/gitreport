"""Generate Excel reports from git commit history."""

import time
from pathlib import Path

import click
from git import Repo
import tablib


def create_report(repo_path: Path, branch: str, xlsx_out_path: Path) -> int:
    """Generate an Excel report of commits from a git repository.

    Args:
        repo_path: Path to the git repository.
        branch: Branch name to generate report for.
        xlsx_out_path: Output path for the Excel file.

    Returns:
        Number of commits included in the report.
    """
    repo = Repo(repo_path)
    headers = ("Date", "Task", "Lines of Code", "Author")
    data = []

    for commit in reversed(list(repo.iter_commits(branch))):
        date = time.strftime("%Y-%m-%d %H:%M", time.gmtime(commit.committed_date))
        msg = commit.message.strip().splitlines()[0]
        msg = msg[0].upper() + msg[1:] if msg else ""
        loc = commit.stats.total["lines"]
        author = commit.author.name
        data.append((date, msg, loc, author))

    table = tablib.Dataset(*data, headers=headers)
    xlsx_out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(xlsx_out_path, "wb") as f:
        f.write(table.export("xlsx"))

    return len(data)


@click.command()
@click.argument("repo_path", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("branch")
@click.argument("output", type=click.Path(dir_okay=False, path_type=Path))
def main(repo_path: Path, branch: str, output: Path):
    """Generate an Excel report of git commits.

    REPO_PATH: Path to the git repository.

    BRANCH: Branch name to generate report for.

    OUTPUT: Output path for the Excel file (.xlsx).
    """
    if not output.suffix:
        output = output.with_suffix(".xlsx")

    click.echo(f"Generating report for {repo_path} ({branch})...")
    count = create_report(repo_path, branch, output)
    click.echo(f"Wrote {count} commits to {output}")


if __name__ == "__main__":
    main()
