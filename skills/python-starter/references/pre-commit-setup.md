# Pre-commit Setup Guide

## Pre-commit Installation and Setup

```bash
# Install pre-commit (dev dependency)
# When using venv
pip install --upgrade pre-commit

# When using poetry
poetry add --group dev pre-commit

# When using uv
uv pip install --system pre-commit
# Or add to pyproject.toml then uv sync --dev
```

## .pre-commit-config.yaml Examples

### Basic (ruff only)

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
```

### Ruff + ty

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/RobertCraigie/ty-python
    rev: v1.1.0
    hooks:
      - id: ty
```

## Pre-commit Installation Commands

After creating the configuration file:

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files once (optional)
pre-commit run --all-files
```
