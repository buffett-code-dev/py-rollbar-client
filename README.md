# py-rollbar-client

[![Latest Release](https://img.shields.io/github/v/release/buffett-code-dev/py-rollbar-client)](https://github.com/buffett-code-dev/py-rollbar-client/releases/latest)

A lightweight Python wrapper for the Rollbar SDK.

## Usage

### Initialization

> **Note:** Do not instantiate `RollbarClient` directly. Always use `init()` / `get_instance()` to ensure `rollbar.init()` is called only once.

Call `init()` once at application startup:

```python
import bc_rollbar_client

bc_rollbar_client.init(access_token="YOUR_TOKEN", environment="production")
```

### Reporting

Use `get_instance()` anywhere to access the initialized client:

```python
from bc_rollbar_client import get_instance, RollbarLevel

client = get_instance()

# Report a message
client.report_message("Something went wrong", level=RollbarLevel.WARNING)

# Report a message with extra data
client.report_message("User error", extra_data={"user_id": "123"})

# Report an exception (must be called within an except block)
try:
    do_something()
except Exception:
    client.report_exception(level=RollbarLevel.ERROR)
```

## Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/). PR titles are validated by CI.

| Prefix | Purpose | Version Bump |
|--------|---------|--------------|
| `feat:` | New feature | Minor |
| `fix:` | Bug fix | Patch |
| `chore:` | Maintenance (deps, CI, etc.) | None |
| `docs:` | Documentation | None |
| `refactor:` | Code refactoring | None |
| `test:` | Tests | None |

Breaking changes: add `!` after the prefix (e.g., `feat!:`) for a major version bump.

## Releasing

This project uses [release-please](https://github.com/googleapis/release-please) for automated releases. To create a release, manually trigger the ["Release Please" workflow](https://github.com/buffett-code-dev/py-rollbar-client/actions/workflows/release-please.yml) from the Actions tab. This will create/update a release PR. Merging the release PR will:

1. Bump the version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a GitHub Release with a git tag (e.g., `v0.2.0`)
