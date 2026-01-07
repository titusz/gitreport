# gitreport

Generate Excel reports from git commit history.

## Installation

Install as a tool using [uv](https://docs.astral.sh/uv/):

```bash
uv tool install git+https://github.com/titusz/gitreport
```

## Usage

```bash
gitreport <repo_path> <branch> <output.xlsx>
```

### Example

```bash
gitreport ./my-project main report.xlsx
```

This generates an Excel file with columns:
- **Date** - Commit timestamp
- **Task** - First line of commit message
- **Lines of Code** - Total lines changed
- **Author** - Commit author name

## One-off Execution

Run without installing:

```bash
uvx --from git+https://github.com/titusz/gitreport gitreport ./my-project main report.xlsx
```

## License

MIT
