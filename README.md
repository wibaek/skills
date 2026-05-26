# Agent Skills

A collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities.

Skills follow the [Agent Skills format](https://github.com/cursor/agent-skills).

## Available Skills

### react-best-practices

React and Next.js performance optimization guidelines from Vercel Engineering. Contains 40+ rules across 8 categories, prioritized by impact.

**Use when:**

- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Optimizing bundle size or load times

**Categories covered:**

- Eliminating waterfalls (Critical)
- Bundle size optimization (Critical)
- Server-side performance (High)
- Client-side data fetching (Medium-High)
- Re-render optimization (Medium)
- Rendering performance (Medium)
- JavaScript micro-optimizations (Low-Medium)

### web-design-guidelines

Review UI code for compliance with web interface best practices. Audits your code for 100+ rules covering accessibility, performance, and UX.

**Use when:**

- "Review my UI"
- "Check accessibility"
- "Audit design"
- "Review UX"
- "Check my site against best practices"

**Categories covered:**

- Accessibility (aria-labels, semantic HTML, keyboard handlers)
- Focus States (visible focus, focus-visible patterns)
- Forms (autocomplete, validation, error handling)
- Animation (prefers-reduced-motion, compositor-friendly transforms)
- Typography (curly quotes, ellipsis, tabular-nums)
- Images (dimensions, lazy loading, alt text)
- Performance (virtualization, layout thrashing, preconnect)
- Navigation & State (URL reflects state, deep-linking)
- Dark Mode & Theming (color-scheme, theme-color meta)
- Touch & Interaction (touch-action, tap-highlight)
- Locale & i18n (Intl.DateTimeFormat, Intl.NumberFormat)

### react-native-guidelines

React Native best practices optimized for AI agents. Contains 16 rules across 7 sections covering performance, architecture, and platform-specific patterns.

**Use when:**

- Building React Native or Expo apps
- Optimizing mobile performance
- Implementing animations or gestures
- Working with native modules or platform APIs

**Categories covered:**

- Performance (Critical) - FlashList, memoization, heavy computation
- Layout (High) - flex patterns, safe areas, keyboard handling
- Animation (High) - Reanimated, gesture handling
- Images (Medium) - expo-image, caching, lazy loading
- State Management (Medium) - Zustand patterns, React Compiler
- Architecture (Medium) - monorepo structure, imports
- Platform (Medium) - iOS/Android specific patterns

### composition-patterns

React composition patterns that scale. Helps avoid boolean prop proliferation through compound components, state lifting, and internal composition.

**Use when:**

- Refactoring components with many boolean props
- Building reusable component libraries
- Designing flexible APIs
- Reviewing component architecture

**Patterns covered:**

- Extracting compound components
- Lifting state to reduce props
- Composing internals for flexibility
- Avoiding prop drilling

### vercel-deploy-claimable

Deploy applications and websites to Vercel instantly. Designed for use with claude.ai and Claude Desktop to enable deployments directly from conversations. Deployments are "claimable" - users can transfer ownership to their own Vercel account.

**Use when:**

- "Deploy my app"
- "Deploy this to production"
- "Push this live"
- "Deploy and give me the link"

**Features:**

- Auto-detects 40+ frameworks from package.json
- Returns preview URL (live site) and claim URL (transfer ownership)
- Handles static HTML projects automatically
- Excludes node_modules and .git from uploads

**How it works:**

1. Packages your project into a tarball
2. Detects framework (Next.js, Vite, Astro, etc.)
3. Uploads to deployment service
4. Returns preview URL and claim URL

**Output:**

```
Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...
```

### python-starter

Automatically configures formatter and linter settings when initializing Python projects. Installs ruff by default and uses pyproject.toml for configuration. Detects or recommends uv/poetry/venv environments and installs dev dependencies. Optionally configures pre-commit and ty (type checker). Suggests VSCode workspace settings when using VSCode.

**Use when:**

- "Start a Python project"
- "Create a FastAPI project"
- "Create a data analysis Python project"
- "Set up Python project with linting"
- "Initialize Python project with ruff"

**Features:**

- **Environment detection**: Automatically detects uv, Poetry, or venv. Recommends uv if no environment is configured
- **Ruff setup**: Installs and configures ruff (formatter + linter) by default
- **Type checking**: Optional ty (type checker) setup with configuration
- **Pre-commit**: Optional pre-commit hooks setup
- **VSCode integration**: Suggests workspace settings for optimal editor experience
- **pyproject.toml**: All configuration stored in pyproject.toml (modern Python standard)

**Workflow:**

1. Detects or recommends environment (uv/poetry/venv)
2. Installs ruff as dev dependency
3. Configures pyproject.toml with ruff settings
4. Optionally sets up ty (type checker)
5. Optionally configures pre-commit hooks
6. Suggests VSCode settings if applicable

### ts-starter

Automatically configures TypeScript project quality tooling without scaffolding applications. Uses pnpm by default when no lockfile exists, preserves existing package managers, and sets up TypeScript, Biome (lint/format), and Vitest with strict-and-safety defaults.

**Use when:**

- "Start a TypeScript project setup"
- "Set up TS lint/format/test"
- "Configure Node TypeScript starter"
- "Standardize TypeScript tooling"
- "Set up Vite TypeScript config"

**Features:**

- **Config-only workflow**: Focuses on quality tooling configuration, not framework app scaffolding
- **Package manager policy**: pnpm-first for new projects, lockfile-aware for existing projects
- **TypeScript baseline**: ESM defaults and strict-and-safety compiler options
- **Biome setup**: Unified lint and format configuration with standard scripts
- **Vitest setup**: Default test runner across frontend, node-app, and library projects
- **Optional extras**: VSCode workspace settings and Husky/lint-staged Git hooks on demand

**Workflow:**

1. Detect package manager (pnpm preferred, preserve existing lockfile manager)
2. Detect project kind (frontend, node-app, library)
3. Install TypeScript, Biome, and Vitest baseline dependencies
4. Apply strict `tsconfig.json`, `biome.json`, and `vitest.config.ts`
5. Optionally configure VSCode settings and Git hooks
6. Validate with typecheck, lint, and test commands

### git-commit-writer

Drafts Conventional Commit messages from the actual git diff and supports a safe commit workflow that avoids unrelated files.

**Use when:**

- "커밋 메시지 만들어줘"
- "이 변경사항으로 커밋해줘"
- "Conventional Commit 형식으로 정리해줘"
- Reviewing staged changes before committing

**Features:**

- Infers the correct commit type from the diff
- Recommends scopes only when they improve clarity
- Preserves unrelated work by focusing on staged or task-relevant files
- Adds a commit body only when reasoning or tradeoffs need explanation

### github-pr-writer

Drafts GitHub pull request titles and structured PR bodies from branch history, diff summaries, and validation results.

**Use when:**

- "PR 본문 작성해줘"
- "이 브랜치로 PR 열어줘"
- "현재 변경사항을 리뷰용으로 요약해줘"
- Preparing `gh pr create` input

**Features:**

- Builds PR context from branch and diff evidence
- Fills a consistent `요약 / 변경 사항 / 검증 / 노트` template
- Keeps validation notes accurate instead of inventing test results
- Calls out mixed or unrelated work before opening the PR

### api-error-standard

Standardizes API error responses using RFC 9457 and RFC 7807 (Problem Details for HTTP APIs). Recommends libraries and patterns for Python, JavaScript/TypeScript, and Java to catch exceptions and return `application/problem+json`.

**Use when:**

- Implementing or refactoring API error handling
- Adding exception handlers that return a consistent error format
- Working with RFC 7807, RFC 9457, problem details, or standardized error responses

**Covered:**

- Problem details object (type, title, status, detail, instance, extensions)
- Python: httpproblem, fastapi-rfc7807
- JavaScript/TypeScript: rfc-7807-problem-details (Express/Koa/Oak)
- Java: Spring ProblemDetail, ErrorResponse, ResponseEntityExceptionHandler
- Validation errors (422) with pointer/detail extensions

## Installation

```bash
npx skills add wibaek/skills
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**

- "Start a Python project"
- "Create a FastAPI project"
- "Create a data analysis Python project"
- "Set up Python project with linting"
- "Initialize Python project with ruff"
- "Set up TS lint/format/test"
- "Configure Node TypeScript starter"

## Skill Structure

Skills are grouped by category:

- `skills/personal/` - personal workflow and project setup preferences
- `skills/general/` - reusable technical standards and guidelines
- `skills/superpowers/` - process-oriented workflow skills

Each skill contains:

- `SKILL.md` - Instructions for the agent
- `assets/` - Template files and configuration examples (optional)
- `references/` - Supporting documentation (optional)
- `scripts/` - Helper scripts for automation (optional)

## License

MIT
