# pyproject.toml Configuration Examples

## Basic ruff Configuration

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "A", "C4", "DTZ", "T10", "EM", "ISC", "ICN", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SIM", "ARG", "PTH", "ERA", "PD", "PGH", "PL", "TRY", "NPY", "RUF"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## ruff + ty Configuration

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "A", "C4", "DTZ", "T10", "EM", "ISC", "ICN", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SIM", "ARG", "PTH", "ERA", "PD", "PGH", "PL", "TRY", "NPY", "RUF"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ty]
pythonVersion = "3.11"
typeCheckingMode = "basic"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnusedImport = true
reportUnusedClass = true
reportUnusedFunction = true
reportUnusedVariable = true
```

## Poetry Project Example

```toml
[tool.poetry]
name = "project-name"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"

[tool.poetry.group.dev.dependencies]
ruff = "^0.1.0"
ty = "^1.0.0"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "A", "C4", "DTZ", "T10", "EM", "ISC", "ICN", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SIM", "ARG", "PTH", "ERA", "PD", "PGH", "PL", "TRY", "NPY", "RUF"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## UV Project Example

```toml
[project]
name = "project-name"
version = "0.1.0"
description = ""
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "ruff>=0.1.0",
    "ty>=1.0.0",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "A", "C4", "DTZ", "T10", "EM", "ISC", "ICN", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SIM", "ARG", "PTH", "ERA", "PD", "PGH", "PL", "TRY", "NPY", "RUF"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```
