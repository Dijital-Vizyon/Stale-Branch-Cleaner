# Stale Branch Cleaner

A Python utility to identify and report stale Git branches in your repository. This tool helps maintain repository hygiene by identifying branches that haven't been updated within a specified timeframe.

## Features

- Identifies remote branches that haven't been updated for a configurable period
- Generates detailed JSON reports with branch statistics
- Configurable staleness threshold
- Command-line interface for easy integration into scripts and workflows

## Requirements

- Python 3.6+
- Git installed and accessible from command line
- Access to the Git repository you want to analyze

## Installation

1. Clone this repository or copy `stale-branch-cleaner.py` to your local machine
2. Ensure you have Python 3.6 or higher installed
3. No additional Python packages are required - the script uses only standard library modules

## Usage

Basic usage:
```bash
python stale-branch-cleaner.py /path/to/repository
```

With optional arguments:
```bash
python stale-branch-cleaner.py /path/to/repository --days 60 --output custom_report.json
```

### Command Line Arguments

- `repo_path`: (Required) Path to the Git repository to analyze
- `--days`: (Optional) Number of days without updates to consider a branch stale (default: 90)
- `--output`: (Optional) Custom path for the output report file (default: stale_branches_report.json)

## Output Format

The script generates a JSON report with the following structure:

```json
{
  "generated_at": "2025-01-16T10:00:00",
  "repository": "/path/to/repository",
  "stale_days_threshold": 90,
  "stale_branches_count": 5,
  "stale_branches": [
    {
      "branch": "feature/old-feature",
      "last_commit": "2024-10-01T15:30:00",
      "days_stale": 107
    },
    ...
  ]
}
```

## Error Handling

The script includes error handling for common issues:
- Validates that the specified path contains a Git repository
- Handles Git command execution errors
- Provides clear error messages for troubleshooting

## Limitations

- Only analyzes remote branches (those tracking origin)
- Requires read access to the Git repository
- Does not automatically delete or modify branches
- Relies on Git command-line tools being installed and accessible

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
