# ext-analyzer

A Python tool for analyzing browser extensions.

# Development

## Setup

1. Install uv using one of these methods:

```bash
brew install uv
```

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
winget install --id=astral-sh.uv  -e
```

```bash
pipx install uv
```

2. setup pre-commit hooks

```bash
uv run pre-commit install
```

## Developement tasks

```bash
uv run ruff check .
uv run ruff format .
uv run ruff check --fix .
uv run ruff check --fix --check-only .
uv run ruff check --fix --check-only --diff .
```
