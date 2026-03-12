---
name: git-commit-writer
description: Draft Conventional Commit messages and execute a safe git commit workflow from staged or changed files. Use when Codex needs to create a commit, suggest a commit message, inspect git diff before committing, split changes into sensible commits, or run `git commit` without including unrelated work.
---

# Git Commit Writer

Write clear Conventional Commit messages from the actual git state. Prefer safe staging, precise scopes, and minimal commit bodies.

## Workflow

1. Inspect the repository state before proposing a message.
   - Check `git status --short`.
   - Review staged diff first with `git diff --cached`.
   - If nothing is staged, inspect `git diff` and decide whether staging is required.
   - Do not assume all modified files belong in one commit.

2. Protect unrelated work.
   - Keep user changes that are unrelated to the requested task out of the commit.
   - If the worktree contains multiple concerns, recommend splitting commits.
   - If the requested commit scope is ambiguous, state the assumption before committing.

3. Infer the commit intent from behavior, not filenames alone.
   - `feat`: visible or functional capability added
   - `fix`: bug or regression corrected
   - `refactor`: internal structure improved without behavior change
   - `docs`: documentation updated
   - `test`: tests added or adjusted
   - `chore`: tooling, config, dependencies, CI, maintenance
   - `style`: formatting or non-functional stylistic cleanup

4. Choose a scope only when it improves clarity.
   - Prefer package, feature, domain, or subsystem names such as `auth`, `payment`, `readme`, `ci`.
   - Omit scope when the change is small or spans the whole repository.

5. Write the commit message in this format.
   - `<type>: <subject>`
   - `<type>(<scope>): <subject>`
   - Keep the subject concise and specific.
   - Use present-tense Korean phrasing that reads naturally in a commit log.
   - Avoid trailing periods and vague subjects like `update`, `fix bug`, or `changes`.

6. Add a body only when it materially helps.
   - Use a body for non-obvious reasoning, tradeoffs, migrations, or multi-step fixes.
   - Keep the body brief and explain why the change matters.
   - Separate subject and body with a blank line.

7. Validate before committing when practical.
   - Run the most relevant tests or lint checks for the touched area.
   - If validation was not run, say so explicitly instead of implying confidence.

8. Commit non-interactively when the user wants the commit created.
   - Prefer `git commit -m "<subject>"`.
   - For a body, use multiple `-m` flags instead of opening an editor.
   - Do not amend or rewrite history unless the user explicitly asks.

## Output Rules

- If the user asks for a suggestion only, provide:
  - the recommended commit message
  - a short rationale tied to the diff
  - optional alternatives only when there is real ambiguity
- If the user asks to commit, show the exact message you are about to use, then run the commit.
- If the diff contains multiple independent changes, recommend split commits before proceeding.

## Message Quality Bar

- Prefer behavior-oriented subjects over implementation trivia.
- Mention the affected domain when that helps future readers scan history.
- Keep the message consistent with the actual diff and staged files.
- Do not claim a fix, feature, or refactor that the diff does not support.

## Examples

- `feat(auth): 로그인 만료 토큰 재발급 API 추가`
- `fix(payment): 결제 승인 실패 시 중복 요청 방지`
- `refactor(user): 회원 조회 서비스 책임 분리`
- `docs(readme): 로컬 실행 방법 보완`
- `test(order): 주문 취소 케이스 테스트 추가`
- `chore(ci): PR 검사 워크플로우 정리`

Use a body when needed:

```text
fix(auth): refresh token 만료 검증 오류 수정

기존에는 access token 기준으로 만료를 체크하고 있어
refresh 요청이 정상적으로 처리되지 않는 문제가 있었다.
refresh token 기준으로 검증하도록 수정했다.
```
