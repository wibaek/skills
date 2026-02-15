# Git Hooks Setup Guide

Use this setup only when the user explicitly opts in.

## Install Dependencies

### pnpm

```bash
pnpm add -D husky lint-staged
pnpm husky init
```

### npm

```bash
npm install -D husky lint-staged
npx husky init
```

### yarn

```bash
yarn add -D husky lint-staged
yarn husky init
```

### bun

```bash
bun add -d husky lint-staged
bunx husky init
```

## `package.json` Example

Add or merge this section:

```json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx,mjs,cjs,json}": ["biome check --write --no-errors-on-unmatched"]
  }
}
```

## Pre-commit Hook Pattern

Run lint-staged and typecheck in pre-commit:

```sh
<package-manager> lint-staged && <package-manager> typecheck
```

Test can be added for stricter projects:

```sh
<package-manager> lint-staged && <package-manager> typecheck && <package-manager> test
```

Use package-manager-specific run forms:

- pnpm: `pnpm <script>`
- npm: `npm run <script>`
- yarn: `yarn <script>`
- bun: `bun run <script>`
