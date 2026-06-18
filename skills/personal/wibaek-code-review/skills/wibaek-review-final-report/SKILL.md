---
name: wibaek-review-final-report
description: Internal phase only for wibaek review workflows. Do not use as a top-level review entrypoint. Assembles validated findings into markdown reports, PR comments, and Codex code-comment directives when supported.
---

# Final Review Report

모든 review mode에서 같은 report shape로 수렴한다.

## Workflow

1. confirmed finding과 rejected/deferred candidate를 구분한다.
2. final priority 순서로 finding을 정렬한다: P0, P1, P2, P3, Info.
3. 각 finding에 evidence, validation, impact path, counterevidence, recommendation을 채운다.
4. rejected/deferred surface는 Reviewed Surfaces에 남긴다.
5. Codex runtime이 code review directive를 지원할 때만 actionable finding마다 `::code-comment` directive를 만든다. 지원하지 않으면 normal markdown finding과 file/line reference를 출력한다.
6. report path가 필요한 경우 `../../references/artifact-paths.md`의 final output path에 markdown report를 쓴다.

## Hard Rules

`../../references/shared-hard-rules.md`를 읽고 적용한다.

- rejected candidate를 finding으로 포함하지 않는다.
- proof gap을 숨기지 않는다.
- generic "code smell" category를 쓰지 않는다.
- P1/P0는 validation evidence와 impact path가 report 안에 보여야 한다.
- directive와 markdown report의 title, priority, file, line, explanation이 일치해야 한다.
- directive attribute를 출력하기 전에 double quote를 escape하거나 제거한다.
