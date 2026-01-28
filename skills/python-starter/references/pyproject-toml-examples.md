## Ruff (formatter + linter)

Use the same Ruff config as `assets/pyproject.toml.template`.

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
  "F",              # Pyflakes
  "E4", "E7", "E9", # pycodestyle errors (subset compatible with Black)
  # The entries below are not part of Ruff's default rule selection.
  "I",              # isort
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## ty (type checker)

Add this section when you want type checking. (Keep your Ruff config as-is.)

```toml
[tool.ty]
pythonVersion = "3.12"
typeCheckingMode = "basic"

reportMissingImports = true
reportMissingTypeStubs = false

reportUnusedImport = true
reportUnusedClass = true
reportUnusedFunction = true
reportUnusedVariable = true
```

## uv (PEP 621 project example)

This example shows:
- uv-style dependencies (`[project]`, `[project.optional-dependencies]`)
- Ruff config (same as the template)
- Optional ty config

```toml
[project]
name = "project-name"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = [
  "ruff>=0.14.14",
  "ty>=0.0.14",
]

# Ruff (from `assets/pyproject.toml.template`)
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
  "F",              # Pyflakes
  "E4", "E7", "E9", # pycodestyle errors (subset compatible with Black)
  # The entries below are not part of Ruff's default rule selection.
  "I",              # isort
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

# ty (optional)
[tool.ty]
pythonVersion = "3.12"
typeCheckingMode = "basic"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnusedImport = true
reportUnusedClass = true
reportUnusedFunction = true
reportUnusedVariable = true
```

## Poetry (project example)

This example shows:
- Poetry dependency blocks (`[tool.poetry.*]`)
- Ruff config (same as the template)
- Optional ty config

```toml
[tool.poetry]
name = "project-name"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.12"

[tool.poetry.group.dev.dependencies]
ruff = "^0.14.14"
ty = "^0.0.14"

# Ruff (from `assets/pyproject.toml.template`)
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
  "F",              # Pyflakes
  "E4", "E7", "E9", # pycodestyle errors (subset compatible with Black)
  # The entries below are not part of Ruff's default rule selection.
  "I",              # isort
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

# ty (optional)
[tool.ty]
pythonVersion = "3.12"
typeCheckingMode = "basic"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnusedImport = true
reportUnusedClass = true
reportUnusedFunction = true
reportUnusedVariable = true
```
