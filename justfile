fmt:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run pytest .
	uv run mypy .
	uv run ruff format --check .
	uv run ruff check .
