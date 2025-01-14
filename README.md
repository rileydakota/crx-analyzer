# crx-analyzer

crx-analyzer is a Python tool for analyzing browser extensions through a risk management lens. It is designed to help you understand the risks associated with a browser extension and enable you to make informed decisions about whether to use it. In addition, it can also be used to aid analysts in hunting for potentially malicious extensions.

crx-analyzer was inspired by the [crxcavator](https://crxcavator.io/docs.html#/) tool and uses some of the same risk scoring techniques, but is focused on providing a local, open source implementation that won't have the risk of being taken down/no longer hosted.

The tool works by downloading the zipped extension file (crx) from the respective browser's extension store and then extracting the files to a temporary directory. It parses the manifest.json file to get the extension's permissions and then uses basic pattern matching to extract URLs that are referenced in the extension's code.

crx-analyzer can be used by an analyst and supports a "pretty" output mode to accommodate this. crx-analyzer also supports a "json" output mode that allows for flexible usage in other tools or even in a CI/CD pipeline.

# Installation

crx-analyzer is available on pypi, and can be installed using pip. Python 3.10 or higher is required.

```bash
pip install crx-analyzer
```

# Usage

```bash
crx-analyzer --id eaijffijbobmnonfhilihbejadplhddo --browser chrome --output pretty
```

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

### Run tests
```bash
uv run pytest
```

### Linters and styling

```bash
uv run ruff check .
uv run black
uv run isort
```
