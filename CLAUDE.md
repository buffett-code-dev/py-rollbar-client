# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A lightweight Python wrapper around the Rollbar SDK. The `RollbarClient` class handles SDK initialization and provides synchronous error reporting (waits for each report to be sent before returning).

## Development Commands

```bash
# Install dependencies
uv sync --all-groups

# Run all checks (tests + type check + lint + format)
uv run just test

# Auto-format and auto-fix lint issues
uv run just fmt

# Run individually
uv run pytest .                  # tests only
uv run pytest test/test_client.py::TestRollbarClient::test_init  # single test
uv run mypy .                    # type checking
uv run ruff format --check .     # format check
uv run ruff check .              # lint check
```

## Toolchain

- **Python**: 3.13 (managed via mise)
- **Package manager**: uv
- **Task runner**: just (justfile)
- **Lint/Format**: ruff (line-length=120, select=E,F,I)
- **Type checking**: mypy
- **Testing**: pytest

## Architecture

- `bc_rollbar_client/__init__.py` — `init()` / `get_instance()` module-level accessors for singleton lifecycle management
- `bc_rollbar_client/client.py` — `RollbarClient` class wrapping `rollbar.init`/`report_message`/`report_exc_info`
- `bc_rollbar_client/level.py` — `RollbarLevel` StrEnum (CRITICAL/ERROR/WARNING/INFO/DEBUG)
- `test/test_client.py` — Tests using `unittest.mock.patch` to mock the rollbar module

## Important Conventions

- **Do not instantiate `RollbarClient` directly.** Always use `bc_rollbar_client.init()` / `bc_rollbar_client.get_instance()` to ensure `rollbar.init()` is called only once.
