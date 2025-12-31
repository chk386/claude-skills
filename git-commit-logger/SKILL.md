---
name: git-commit-logger
description: Generate well-formatted, conventional commit messages by analyzing git diff and staged changes. Use when the user asks to create commit messages, analyze changes for commits, generate changelog entries, or needs help writing descriptive git commit logs. Supports both conventional commit format and customizable templates.
---

# Git Commit Logger

## Overview

This skill helps generate meaningful git commit messages by analyzing staged changes (`git diff --cached`) and providing structured, conventional commit messages following best practices.

**Automatic Ticket Integration**: If your branch name follows patterns like `feature/MKPC-0000`, `bugfix/PROJ-123`, or `hotfix/ISSUE-456`, the ticket number will be automatically extracted and added as a prefix to your commit message (e.g., `[MKPC-0000] feat: add new feature`).

## Quick Start

Generate a commit message with automatic staging:

```bash
# Stage all changes and generate commit message in one step
python3 scripts/generate_commit.py --add
```

Or if your changes are already staged:

```bash
# Generate commit message for staged changes
python3 scripts/generate_commit.py
```

The script will:
1. Stage changes with `git add .` (when `--add` flag is used)
2. Detect current branch name and extract ticket number (if present)
3. Analyze staged changes via `git diff --cached`
4. Identify changed files and types of changes
5. Generate a conventional commit message with ticket prefix

### Example with Ticket Number

```bash
# On branch: feature/MKPC-1234 with unstaged changes
$ python3 scripts/generate_commit.py --add

Generated Commit Message:
[MKPC-1234] feat(auth): add user authentication module
```

### Example without Ticket Number

```bash
# On branch: main with unstaged changes
$ python3 scripts/generate_commit.py --add

Generated Commit Message:
docs: update README.md
```

### Using Pre-staged Changes

```bash
# Changes already staged with git add
$ python3 scripts/generate_commit.py

Generated Commit Message:
feat(api): add new endpoint handler
```

## Conventional Commit Format

The skill follows the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc.)
- **refactor**: Code refactoring without feature changes
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system or dependency changes
- **ci**: CI/CD configuration changes
- **chore**: Maintenance tasks

## Advanced Usage

### Custom Templates

For project-specific commit message formats, create a template file:

```bash
python3 scripts/generate_commit.py --template custom_template.txt
```

### Changelog Generation

Generate changelog entries from commit history:

```bash
python3 scripts/generate_changelog.py --from v1.0.0 --to HEAD
```

### Batch Processing

Generate commit messages for multiple feature branches:

```bash
python3 scripts/batch_commit_analysis.py --branches feature/*
```

## Resources

### scripts/generate_commit.py
Main script for analyzing git changes and generating commit messages.

### references/commit_guidelines.md
Detailed guidelines for writing effective commit messages with examples.
