# TypeScript Environment Setup Guide

## Package Manager Detection Rules

Use this order and stop at the first match:

1. `pnpm-lock.yaml` -> `pnpm`
2. `package-lock.json` -> `npm`
3. `yarn.lock` -> `yarn`
4. `bun.lock` or `bun.lockb` -> `bun`
5. No lockfile -> `pnpm` (default)

If multiple lockfiles exist, ask the user which manager is canonical before changing dependencies.

## Baseline Dependency Set

Install these as dev dependencies:

- `typescript`
- `@types/node`
- `@biomejs/biome`
- `vitest`

## Package Manager Commands

### pnpm

```bash
pnpm add -D typescript @types/node @biomejs/biome vitest
```

### npm

```bash
npm install -D typescript @types/node @biomejs/biome vitest
```

### yarn

```bash
yarn add -D typescript @types/node @biomejs/biome vitest
```

### bun

```bash
bun add -d typescript @types/node @biomejs/biome vitest
```

## Respect Existing Manager Policy

- Existing lockfile present: keep that package manager.
- No lockfile: initialize and proceed with `pnpm`.
- Never silently switch lockfile ecosystems.
