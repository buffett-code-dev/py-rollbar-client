# py-rollbar-client

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

# Report a message
get_instance().report_message("Something went wrong", level=RollbarLevel.WARNING)

# Report a message with extra data
get_instance().report_message("User error", extra_data={"user_id": "123"})

# Report an exception (must be called within an except block)
try:
    do_something()
except Exception:
    get_instance().report_exception(level=RollbarLevel.ERROR)
```

## Releasing

This project uses [release-please](https://github.com/googleapis/release-please) for automated releases. To create a release, manually trigger the "Release Please" workflow from the Actions tab. This will create/update a release PR. Merging the release PR will:

1. Bump the version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a GitHub Release with a git tag (e.g., `v0.2.0`)
