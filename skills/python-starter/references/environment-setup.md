# Python Environment Setup Guide

## Environment Selection Criteria

- **venv**: Standard library, suitable for simple projects
- **uv**: Suitable for projects requiring fast speed
- **poetry**: Suitable for projects requiring dependency management and packaging

## Using venv

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (macOS/Linux)
source .venv/bin/activate

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install ruff (dev)
pip install --upgrade ruff

# Install ty (dev, optional)
pip install --upgrade ty
```

## Using UV

```bash
# Initialize UV project
uv init

# Or configure uv for existing project
uv pip install --system ruff ty

# Or after adding dev dependencies to pyproject.toml
uv sync --dev
```

## Using Poetry

```bash
# Initialize Poetry project (existing directory)
poetry init --no-interaction

# Or if pyproject.toml already exists
poetry install

# Add ruff as dev dependency
poetry add --group dev ruff

# Add ty as dev dependency (optional)
poetry add --group dev ty

# Activate virtual environment
poetry shell
```

## Environment Detection Methods

1. **UV detection**: Check if `uv.lock` file exists or `uv` command is available
2. **Poetry detection**: Check if `[tool.poetry]` section exists in `pyproject.toml`
3. **Default**: Use venv if neither of the above
