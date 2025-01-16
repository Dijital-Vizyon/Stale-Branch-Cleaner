import subprocess
from datetime import datetime, timedelta
import json
import argparse
from pathlib import Path

class StaleBranchCleaner:
    def __init__(self, repo_path: str, stale_days: int = 90):
        """
        Initialize the stale branch cleaner.
        
        Args:
            repo_path (str): Path to the Git repository
            stale_days (int): Number of days without updates to consider a branch stale
        """
        self.repo_path = Path(repo_path)
        self.stale_days = stale_days
        
        if not (self.repo_path / '.git').exists():
            raise ValueError(f"No Git repository found at {repo_path}")

    def get_all_branches(self):
        """Get all local branches in the repository."""
        result = subprocess.run(
            ['git', 'branch', '-r'],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        branches = [
            branch.strip().replace('origin/', '')
            for branch in result.stdout.split('\n')
            if branch and not branch.strip().endswith('HEAD')
        ]
        return branches

    def get_last_commit_date(self, branch: str):
        """Get the date of the last commit on a branch."""
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%at', f'origin/{branch}'],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        timestamp = int(result.stdout.strip())
        return datetime.fromtimestamp(timestamp)

    def identify_stale_branches(self):
        """Identify branches that haven't been updated within the stale_days period."""
        cutoff_date = datetime.now() - timedelta(days=self.stale_days)
        stale_branches = []
        
        for branch in self.get_all_branches():
            last_commit_date = self.get_last_commit_date(branch)
            if last_commit_date < cutoff_date:
                stale_branches.append({
                    'branch': branch,
                    'last_commit': last_commit_date.isoformat(),
                    'days_stale': (datetime.now() - last_commit_date).days
                })
        
        return stale_branches

    def generate_report(self, output_file: str = 'stale_branches_report.json'):
        """Generate a report of stale branches."""
        stale_branches = self.identify_stale_branches()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'repository': str(self.repo_path),
            'stale_days_threshold': self.stale_days,
            'stale_branches_count': len(stale_branches),
            'stale_branches': sorted(
                stale_branches,
                key=lambda x: x['days_stale'],
                reverse=True
            )
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report

def main():
    parser = argparse.ArgumentParser(description='Identify stale Git branches')
    parser.add_argument('repo_path', help='Path to the Git repository')
    parser.add_argument(
        '--days',
        type=int,
        default=90,
        help='Number of days without updates to consider a branch stale'
    )
    parser.add_argument(
        '--output',
        default='stale_branches_report.json',
        help='Output file path for the report'
    )
    
    args = parser.parse_args()
    
    try:
        cleaner = StaleBranchCleaner(args.repo_path, args.days)
        report = cleaner.generate_report(args.output)
        
        print(f"\nStale Branch Report Summary:")
        print(f"Repository: {report['repository']}")
        print(f"Threshold: {report['stale_days_threshold']} days")
        print(f"Stale branches found: {report['stale_branches_count']}")
        print(f"\nFull report saved to: {args.output}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
