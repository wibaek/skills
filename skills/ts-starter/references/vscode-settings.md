# VSCode Workspace Settings Guide

Suggest this setup only when the user wants VSCode integration.

## `.vscode/settings.json` Example

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "biomejs.biome",
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

## Recommended VSCode Extensions

1. **Biome** (`biomejs.biome`)
2. **TypeScript and JavaScript Language Features** (built-in)
3. **Vitest** (`vitest.explorer`) - optional

## File Placement

Create `.vscode/settings.json` in the project root.
