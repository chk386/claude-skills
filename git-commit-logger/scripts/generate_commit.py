#!/usr/bin/env python3
"""
Git Commit Message Generator

Analyzes staged git changes and generates a conventional commit message.

Usage:
    python3 generate_commit.py [--template TEMPLATE_FILE] [--interactive]
"""

import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


# Conventional commit types
COMMIT_TYPES = {
    'feat': 'New feature',
    'fix': 'Bug fix',
    'docs': 'Documentation changes',
    'style': 'Code style changes',
    'refactor': 'Code refactoring',
    'perf': 'Performance improvements',
    'test': 'Test changes',
    'build': 'Build system changes',
    'ci': 'CI/CD changes',
    'chore': 'Maintenance tasks'
}


def run_git_command(command: List[str]) -> str:
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            ['git'] + command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}", file=sys.stderr)
        sys.exit(1)


def get_staged_diff() -> str:
    """Get the diff of staged changes."""
    return run_git_command(['diff', '--cached'])


def get_staged_files() -> List[str]:
    """Get list of staged files."""
    output = run_git_command(['diff', '--cached', '--name-only'])
    return [f for f in output.strip().split('\n') if f]


def get_current_branch() -> str:
    """Get current git branch name."""
    try:
        output = run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
        return output.strip()
    except:
        return ''


def extract_ticket_number(branch_name: str) -> str:
    """
    Extract ticket number from branch name.
    
    Supports patterns like:
    - feature/MKPC-0000
    - bugfix/MKPC-1234
    - hotfix/PROJ-999
    
    Returns empty string if no ticket found.
    """
    if not branch_name:
        return ''
    
    # Pattern: feature/MKPC-0000, bugfix/PROJ-123, etc.
    match = re.search(r'([A-Z]+-\d+)', branch_name)
    if match:
        return match.group(1)
    
    return ''


def analyze_changes(diff: str, files: List[str]) -> Dict[str, any]:
    """Analyze the git diff and categorize changes."""
    analysis = {
        'files': files,
        'additions': diff.count('\n+') - diff.count('\n+++'),
        'deletions': diff.count('\n-') - diff.count('\n---'),
        'file_types': set(),
        'directories': set(),
        'likely_type': 'chore'
    }
    
    # Analyze file types and directories
    for file in files:
        path = Path(file)
        if path.suffix:
            analysis['file_types'].add(path.suffix)
        if path.parent != Path('.'):
            analysis['directories'].add(str(path.parent))
    
    # Determine likely commit type based on patterns
    if any('.md' in f or 'README' in f or 'doc' in f.lower() for f in files):
        analysis['likely_type'] = 'docs'
    elif 'test' in str(analysis['directories']) or any('test' in f.lower() for f in files):
        analysis['likely_type'] = 'test'
    elif '.yml' in analysis['file_types'] or '.yaml' in analysis['file_types']:
        if any('ci' in str(d) or '.github' in str(d) for d in analysis['directories']):
            analysis['likely_type'] = 'ci'
        else:
            analysis['likely_type'] = 'build'
    elif re.search(r'(fix|bug|issue|patch)', diff, re.IGNORECASE):
        analysis['likely_type'] = 'fix'
    elif re.search(r'(add|new|feature|implement)', diff, re.IGNORECASE):
        analysis['likely_type'] = 'feat'
    elif re.search(r'(refactor|restructure|reorganize)', diff, re.IGNORECASE):
        analysis['likely_type'] = 'refactor'
    
    return analysis


def determine_scope(analysis: Dict) -> str:
    """Determine the scope based on changed directories."""
    dirs = analysis['directories']
    if len(dirs) == 1:
        return list(dirs)[0].split('/')[-1]
    elif len(dirs) > 1:
        # Find common prefix
        common = Path(sorted(dirs)[0])
        if common.name:
            return common.name
    return ''


def generate_subject(commit_type: str, scope: str, files: List[str], analysis: Dict) -> str:
    """Generate a commit subject line."""
    if len(files) == 1:
        file_desc = f"update {Path(files[0]).name}"
    elif len(files) <= 3:
        file_desc = f"update {', '.join(Path(f).name for f in files[:3])}"
    else:
        file_desc = f"update {len(files)} files"
    
    # Customize based on commit type
    if commit_type == 'feat':
        subject = f"add new feature in {scope or 'module'}"
    elif commit_type == 'fix':
        subject = f"resolve issue in {scope or 'module'}"
    elif commit_type == 'docs':
        subject = file_desc
    else:
        subject = file_desc
    
    return subject[:50]  # Limit to 50 characters


def generate_body(analysis: Dict) -> str:
    """Generate the commit message body."""
    lines = []
    
    if analysis['files']:
        lines.append("Changes:")
        for file in sorted(analysis['files'])[:10]:  # Show up to 10 files
            lines.append(f"  - {file}")
        if len(analysis['files']) > 10:
            lines.append(f"  ... and {len(analysis['files']) - 10} more files")
    
    lines.append("")
    lines.append(f"Modified: {analysis['additions']}+ / {analysis['deletions']}- lines")
    
    return '\n'.join(lines)


def generate_commit_message(analysis: Dict, commit_type: str = None, ticket_number: str = '') -> str:
    """Generate a complete conventional commit message."""
    if commit_type is None:
        commit_type = analysis['likely_type']
    
    scope = determine_scope(analysis)
    subject = generate_subject(commit_type, scope, analysis['files'], analysis)
    
    # Build commit message header
    header = f"{commit_type}"
    if scope:
        header += f"({scope})"
    header += f": {subject}"
    
    # Add ticket number prefix if available
    if ticket_number:
        header = f"[{ticket_number}] {header}"
    
    body = generate_body(analysis)
    
    return f"{header}\n\n{body}"


def interactive_mode(analysis: Dict, ticket_number: str = '') -> str:
    """Interactive mode to let user customize the commit message."""
    print("\n=== Git Commit Message Generator ===\n")
    
    if ticket_number:
        print(f"📌 Detected ticket: {ticket_number}")
    
    print(f"Detected changes in {len(analysis['files'])} files")
    print(f"Suggested type: {analysis['likely_type']}")
    print(f"\nAvailable types:")
    for i, (typ, desc) in enumerate(COMMIT_TYPES.items(), 1):
        marker = "→" if typ == analysis['likely_type'] else " "
        print(f"  {marker} {i}. {typ:10s} - {desc}")
    
    print("\nPress Enter to use suggested type, or enter number (1-10):")
    choice = input().strip()
    
    if choice and choice.isdigit():
        types_list = list(COMMIT_TYPES.keys())
        idx = int(choice) - 1
        if 0 <= idx < len(types_list):
            commit_type = types_list[idx]
        else:
            commit_type = analysis['likely_type']
    else:
        commit_type = analysis['likely_type']
    
    return generate_commit_message(analysis, commit_type, ticket_number)


def main():
    """Main entry point."""
    # Check if there are staged changes
    staged_files = get_staged_files()
    if not staged_files:
        print("No staged changes found. Use 'git add' to stage changes first.")
        sys.exit(1)
    
    # Get current branch and extract ticket number
    branch_name = get_current_branch()
    ticket_number = extract_ticket_number(branch_name)
    
    # Get diff and analyze
    diff = get_staged_diff()
    analysis = analyze_changes(diff, staged_files)
    
    # Check for interactive mode
    interactive = '--interactive' in sys.argv or '-i' in sys.argv
    
    if interactive:
        message = interactive_mode(analysis, ticket_number)
    else:
        message = generate_commit_message(analysis, ticket_number=ticket_number)
    
    # Output the commit message
    print("\n" + "="*60)
    print("Generated Commit Message:")
    print("="*60)
    print(message)
    print("="*60)
    
    # Show usage instructions
    commit_msg_preview = message.split('\n')[0]
    print("\nTo use this message:")
    print(f"  git commit -m '{commit_msg_preview}'")
    print("\nOr for multi-line commit:")
    print("  git commit")
    print("  # Then paste the full message in your editor")


if __name__ == "__main__":
    main()
