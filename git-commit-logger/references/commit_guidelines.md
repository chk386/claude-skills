# Git Commit Message Guidelines

## Best Practices

### 0. 항상 한글로 작성해줘
commit message는 항상 한글로 작성해야만 해

### 1. Use the Imperative Mood
Write commit messages as commands: "Add feature" not "Added feature" or "Adding feature"

✅ Good: `fix: resolve memory leak in data processor`
❌ Bad: `fix: resolved memory leak in data processor`

### 2. Keep Subject Line Short
- Maximum 50 characters for subject line
- Use body for additional details
- Separate subject and body with blank line

### 3. Capitalize Subject Line
Always start the subject with a capital letter

✅ Good: `feat: Add user authentication`
❌ Bad: `feat: add user authentication`

### 4. No Period at End of Subject
The subject line should not end with a period

✅ Good: `docs: Update README with installation steps`
❌ Bad: `docs: Update README with installation steps.`

## Commit Message Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (Required)
- **feat**: A new feature for the user
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (white-space, formatting)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

### Scope (Optional)
The scope should be the name of the affected module, component, or area:
- `auth`: Authentication module
- `api`: API layer
- `db`: Database layer
- `ui`: User interface
- `config`: Configuration files

### Subject (Required)
- Concise description of the change
- Use imperative mood
- Don't capitalize first letter after the colon
- No period at the end
- Maximum 50 characters

### Body (Optional)
- Provide additional context
- Explain the what and why, not the how
- Wrap at 72 characters
- Separate from subject with blank line

### Footer (Optional)
- Reference issue tracker IDs
- Note breaking changes
- Format: `BREAKING CHANGE: description` or `Fixes #123`

## Real-World Examples

### Example 1: New Feature
```
feat(auth): add JWT token refresh mechanism

Implement automatic token refresh when access token expires.
This prevents users from being logged out unexpectedly during
active sessions.

The refresh token is stored securely in httpOnly cookie and
rotated on each refresh request.

Closes #234
```

### Example 2: Bug Fix
```
fix(api): prevent race condition in user registration

Add transaction lock to ensure email uniqueness check and
user creation happen atomically. Previously, concurrent
registration attempts could create duplicate users.

Fixes #456
```

### Example 3: Documentation
```
docs: add API rate limiting guidelines

Include examples of rate limit headers and error responses.
Add section on handling 429 Too Many Requests errors.
```

### Example 4: Breaking Change
```
feat(api): change user endpoint response format

BREAKING CHANGE: The /api/users endpoint now returns user
data in a nested 'data' field instead of at the root level.

Before: { "id": 1, "name": "John" }
After: { "data": { "id": 1, "name": "John" } }

Migration guide available in docs/migrations/v2.md
```

### Example 5: Performance Improvement
```
perf(db): add index on user_events.created_at

Query performance improved from 2.3s to 45ms for event
timeline queries. Tested with 10M records.
```

## Common Patterns by File Type

### Configuration Files
```
chore(config): update nginx timeout settings
build(deps): upgrade React to v18.2.0
```

### Tests
```
test(auth): add integration tests for password reset
test: increase test coverage for payment module
```

### Documentation
```
docs: fix typo in installation guide
docs(api): add examples for webhook endpoints
```

### CI/CD
```
ci: add code coverage reporting to GitHub Actions
ci(deploy): automate staging deployment on merge
```

## Tips for Better Commit Messages

1. **Commit Often**: Small, focused commits are easier to review and understand
2. **One Concern Per Commit**: Each commit should address one logical change
3. **Reference Issues**: Link commits to issue tracker when applicable
4. **Explain Why**: The code shows what changed, the commit message explains why
5. **Use Conventional Format**: Consistency helps automation and filtering

## Automated Tools

The skill provides scripts to help generate consistent commit messages:

- `generate_commit.py`: Analyzes changes and suggests commit messages
- `generate_changelog.py`: Creates changelog from commit history
- `validate_commit.py`: Checks if commit message follows conventions

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [Semantic Versioning](https://semver.org/)
