---
name: ts-starter
description: Configure TypeScript project tooling for existing Node or frontend projects without app scaffolding. Use for TS starter setup, TS lint/format/test setup, Node TypeScript starter, or Vite TypeScript config requests.
---

# TypeScript Starter

Automatically configure linting, formatting, testing, and compiler defaults for TypeScript projects.

## Workflow

1. **Detect package manager**
   - Prefer `pnpm` when no lockfile exists.
   - If lockfile exists, keep the existing manager.
   - Detection order:
     1. `pnpm-lock.yaml` -> `pnpm`
     2. `package-lock.json` -> `npm`
     3. `yarn.lock` -> `yarn`
     4. `bun.lock` or `bun.lockb` -> `bun`
   - Ask the user only when detection is ambiguous.

2. **Detect project kind**
   - Classify as `frontend`, `node-app`, or `library`.
   - Use existing files (`vite.config.*`, framework deps, publish fields, entry points) for detection.
   - Ask the user when the project kind is unclear.

3. **Install baseline dependencies**
   - Install as dev dependencies: `typescript`, `@types/node`, `@biomejs/biome`, `vitest`.
   - Use package-manager-specific commands from [references/environment-setup.md](references/environment-setup.md).

4. **Apply TypeScript configuration**
   - Create or update `tsconfig.json` with strict-and-safety defaults.
   - Keep ESM defaults.
   - Preserve existing options whenever possible and patch only missing required fields.
   - Reference: [references/config-examples.md](references/config-examples.md)
   - Template: [assets/tsconfig.json.template](assets/tsconfig.json.template)

5. **Apply Biome configuration**
   - Create or update `biome.json`.
   - Add `lint`, `lint:fix`, and `format` scripts in `package.json` if missing.
   - Keep existing scripts and merge safely.
   - Reference: [references/config-examples.md](references/config-examples.md)
   - Template: [assets/biome.json.template](assets/biome.json.template)

6. **Apply Vitest configuration**
   - Create or update `vitest.config.ts` and test scripts.
   - Use Vitest as the default runner for all project kinds in this skill version.
   - Reference: [references/config-examples.md](references/config-examples.md)
   - Template: [assets/vitest.config.ts.template](assets/vitest.config.ts.template)

7. **Optional VSCode settings**
   - Ask whether to add `.vscode/settings.json`.
   - Reference: [references/vscode-settings.md](references/vscode-settings.md)
   - Template: [assets/.vscode-settings.json.template](assets/.vscode-settings.json.template)

8. **Optional Git hooks**
   - Ask whether to set up Husky + lint-staged.
   - Configure pre-commit for lint and typecheck (test optional).
   - Reference: [references/git-hooks-setup.md](references/git-hooks-setup.md)
   - Template: [assets/.husky-pre-commit.template](assets/.husky-pre-commit.template)

9. **Update ignore rules**
   - Create or patch `.gitignore` for common TypeScript/Node artifacts.
   - Template: [assets/.gitignore.template](assets/.gitignore.template)

10. **Run smoke validation**
   - Run `typecheck`, `lint`, and `test` once after setup.
   - Keep commands package-manager-specific.

## Principles

- **Config-only**: Do not scaffold framework applications by default.
- **Command-first**: Prefer commands over manual editing when possible.
- **Idempotent updates**: Re-running setup must not duplicate scripts or corrupt config.
- **Preserve existing intent**: Merge with current project configuration and patch only required pieces.

## Internal Contracts

- `project_kind`: `frontend | node-app | library`
- `package_manager`: `pnpm | npm | yarn | bun`

## References

- **Environment setup**: [references/environment-setup.md](references/environment-setup.md)
- **Configuration examples**: [references/config-examples.md](references/config-examples.md)
- **Git hooks setup**: [references/git-hooks-setup.md](references/git-hooks-setup.md)
- **VSCode settings**: [references/vscode-settings.md](references/vscode-settings.md)
