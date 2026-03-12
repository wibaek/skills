---
name: github-pr-writer
description: Draft GitHub pull request titles and structured PR bodies from branch history, diffs, and validation results. Use when Codex needs to write a PR description, summarize a branch for review, choose a base branch, prepare `gh pr create`, or open a pull request that follows the repository template.
---

# GitHub PR Writer

Summarize a branch into a reviewable pull request with a precise title, a structured body, and accurate validation notes. Base the write-up on git evidence, not guesswork.

## Workflow

1. Build PR context from git.
   - Check `git status --short` for uncommitted work.
   - Identify the current branch.
   - Determine the comparison target from repository conventions, existing tracking branch, or explicit user instruction.
   - Inspect the branch delta with commit history and diff summary before writing.

2. Protect accuracy.
   - Base the PR on committed changes whenever possible.
   - If important work is still uncommitted, say that the PR description may be incomplete.
   - Do not invent motivation, implementation details, or validation results that are not supported by the branch.

3. Write a concise PR title.
   - Match repository conventions when visible.
   - Otherwise write a short, specific title that describes the user-facing or reviewer-relevant outcome.
   - Avoid noisy prefixes unless the repository already uses them.

4. Fill the PR body with this structure.

```md
## 요약
- ...
- ...

## 변경 사항
- ...

## 검증
- ...

## 노트
- ...
```

5. Apply section rules.
   - `요약`: write 2-4 bullets explaining why the PR exists and what changed.
   - `변경 사항`: list concrete implementation changes reviewers should inspect.
   - `검증`: include commands run, tests performed, or manual checks completed.
   - `노트`: add rollout concerns, follow-ups, review hints, screenshots, or `- 없음` when there is nothing useful to add.

6. Keep reviewer value high.
   - Emphasize externally visible behavior, migrations, risks, and non-obvious design choices.
   - Collapse low-signal edit inventory into broader bullets.
   - Mention untouched but relevant areas only when they affect review or rollout.

7. Create the PR only when asked.
   - If the user wants the actual PR opened, prepare the final title and body first.
   - Prefer non-interactive GitHub CLI usage such as `gh pr create --title ... --body-file ...`.
   - Do not open or update a PR if authentication, base branch, or remote target is unclear without stating the assumption.

## Evidence Collection

- Prefer `git log --oneline <base>..HEAD` to understand commit intent.
- Prefer `git diff --stat <base>...HEAD` and targeted diff reads to understand scope.
- Use recent test output or commands you ran in the current session for `검증`.
- If no validation was run, write that explicitly in `검증`.

## Output Rules

- If the user asks for a draft only, provide the title and complete PR body in Markdown.
- If the user asks to open the PR, present the title/body you will use and then run the create command.
- If the branch mixes unrelated work, call that out and recommend splitting before opening the PR.

## Quality Bar

- Make every bullet useful to a reviewer.
- Keep the body aligned with the actual branch delta.
- Prefer concrete nouns and verbs over generic phrases like `update logic` or `improve stuff`.
- Do not paste raw commit history when a synthesized summary is clearer.
