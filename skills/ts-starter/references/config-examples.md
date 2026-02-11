# TypeScript Config Examples

## Standard `package.json` Scripts

Use these scripts as baseline. Add missing scripts without removing existing project-specific scripts.

```json
{
  "typecheck": "tsc --noEmit",
  "build": "tsc -p tsconfig.json",
  "lint": "biome check .",
  "lint:fix": "biome check --write .",
  "format": "biome format --write .",
  "test": "vitest run",
  "test:watch": "vitest"
}
```

## Strict+Safety `tsconfig.json` Baseline

Use this as a default for Node and frontend projects. Keep ESM defaults.

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2023"],
    "types": ["node", "vitest/globals"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "useUnknownInCatchVariables": true,
    "resolveJsonModule": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true,
    "declaration": true,
    "sourceMap": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src", "test", "vitest.config.ts"],
  "exclude": ["dist", "node_modules"]
}
```

For frontend projects, add framework-specific options such as `jsx` only when required.

## Biome `biome.json` Example

```json
{
  "$schema": "https://biomejs.dev/schemas/latest/schema.json",
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "semicolons": "always"
    }
  }
}
```

## Vitest `vitest.config.ts` Example

```ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    include: ["src/**/*.test.ts", "test/**/*.test.ts"]
  }
});
```
