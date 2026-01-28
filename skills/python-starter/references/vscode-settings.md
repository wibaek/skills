# VSCode Workspace Settings Guide

## .vscode/settings.json Examples

### Basic Settings (ruff only)

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "ruff.enable": true,
  "ruff.format.args": [],
  "ruff.lint.args": []
}
```

### Ruff + ty Settings

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "ruff.enable": true,
  "ruff.format.args": [],
  "ruff.lint.args": [],
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.diagnosticMode": "workspace"
}
```

## Required VSCode Extensions

Suggest the following extensions to users:

1. **Ruff** (`charliermarsh.ruff`) - Required
2. **Python** (`ms-python.python`) - Required (includes Pylance with ty)

## Configuration File Creation

Suggest creating `.vscode/settings.json` file at the project root.
