---
name: wibaek-review-final-report
description: Internal phase only for wibaek review workflows. Do not use as a top-level review entrypoint. Assembles validated findings into markdown reports, PR comments, and Codex code-comment directives when supported.
---

# Final Review Report

모든 review mode에서 같은 report shape로 수렴한다.
report format은 `references/final-report.md`를 따른다.
repository/scoped/deep review의 primary readable output은 `report.html`이다.

## Workflow

1. confirmed finding과 rejected/deferred candidate를 구분한다.
2. architecture/system design finding과 code/behavior finding을 분리한다.
3. 각 section 안에서 final priority 순서로 finding을 정렬한다: P0, P1, P2, P3, Info.
4. 각 finding에 evidence, validation, impact path, counterevidence, recommendation을 채운다.
5. `wibaek-review-scan` 또는 `wibaek-review-deep-scan`이면 architecture/system design review outcome을 반드시 쓴다.
6. rejected/deferred surface는 Reviewed Surfaces에 남긴다.
7. Codex runtime이 code review directive를 지원할 때만 actionable finding마다 `::code-comment` directive를 만든다. 지원하지 않으면 normal markdown finding과 file/line reference를 출력한다.
8. `references/artifact-paths.md`의 final output path에 `report.md`를 쓴다. 사용자가 명시적으로 artifact 생성을 금지하지 않는 한 콘솔 출력만으로 끝내지 않는다.
9. script가 사용 가능하면 `uv run python <skill_dir>/scripts/validate_review_report.py --report-md <review_dir>/report.md`로 report shape를 검증한다. 실패하면 `<review_dir>/report_validation.md`에 output을 남기고, missing section/field를 채운 뒤 다시 검증한다.
10. script와 template이 사용 가능하면 `uv run python <skill_dir>/scripts/render_review_report_html.py --report-md <review_dir>/report.md --report-html <review_dir>/report.html --title "<repo_or_target> Engineering Review"`로 HTML report를 만든다.
11. final response에는 `report.html`, `report.md`, finding count, 검증 제한만 짧게 쓰고, 사용자가 요청하지 않는 한 전체 report를 다시 붙여 넣지 않는다.

## Hard Rules

`references/shared-hard-rules.md`를 읽고 적용한다.

- rejected candidate를 finding으로 포함하지 않는다.
- proof gap을 숨기지 않는다.
- generic "code smell" category를 쓰지 않는다.
- P1/P0는 validation evidence와 impact path가 report 안에 보여야 한다.
- review-scan/deep-scan에서 architecture/system design section을 생략하지 않는다.
- repository/scoped/deep review에서 최종 답변이 finding bullet list만으로 끝나면 안 된다. `report.md`와 `report.html` artifact가 있어야 한다.
- reportable finding이 적을 때도 후보를 조용히 버리지 않는다. 확정 finding으로 승격하지 않은 plausible candidate는 proof gap과 next validation을 `Follow-up Candidates` 또는 `Reviewed Surfaces`에 남긴다.
- finding 수를 채우려고 weak candidate를 P2 이상으로 올리지 않는다. 대신 confidence, proof gap, next validation을 visible하게 만든다.
- directive와 markdown report의 title, priority, file, line, explanation이 일치해야 한다.
- directive attribute를 출력하기 전에 double quote를 escape하거나 제거한다.
