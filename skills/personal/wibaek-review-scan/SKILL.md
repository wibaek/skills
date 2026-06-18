---
name: wibaek-review-scan
description: Review an entire codebase, scoped code area, system design, architecture design, ADR, RFC, or design doc for engineering risks. Use for broad code/system/architecture reviews, not ordinary Git-only diffs.
---

# Review Scan

전체 코드, scoped path/package/module/folder/service boundary, 시스템 디자인, 아키텍처 디자인,
architecture document, design document, ADR, RFC 리뷰에 사용한다.
ordinary PR diff feedback에는 `wibaek-review-diff-scan`을 사용한다.

## Phase 순서

1. `wibaek-review-baseline`
2. `wibaek-review-discovery`
3. `wibaek-review-validation`
4. `wibaek-review-impact-analysis`
5. `wibaek-review-final-report`

phase를 합치지 않는다. 모든 in-scope surface를 다 봤다고 주장하려면 coverage artifact가 있어야 한다.

## Goal Setup

standard 또는 deep repository, scoped path, module, service boundary, 또는 document review 작업 전에 `references/goal-setup.md`의 `wibaek-review-scan` objective로 Codex goal을 생성하거나 호환되는 active goal을 이어받는다. 작은 scoped/document quick review에서는 goal이 필요 없다.

goal을 사용하는 standard/deep mode에서는 모든 in-scope file, surface, document section, 또는 worklist row가 completion receipt나 명시적 deferred closure를 가져야 하고, discovery candidate는 validation 및 impact analysis receipt 또는 rejected/deferred reason을 가져야 하며, final report가 작성 또는 final response에 포함되어야 한다.

## Scope Resolution

다음 중 하나로 scope를 해석한다.

- entire codebase
- full repository
- scoped path
- package or module
- service boundary
- system design
- architecture design
- architecture layer
- runtime surface such as API, worker, CLI, batch, frontend app
- document target such as ADR, RFC, design proposal, architecture writeup

문서 target이면 `references/design-doc-review.md`도 읽는다.

scope가 한 번에 너무 크면 runtime surface 또는 module 단위로 나누고 deferred area를 명시한다.

## Baseline

생성 또는 업데이트한다.

- AGENTS.md, README, ADR, docs, API contract, test name에서 추출한 declared intent
- prevalence note가 포함된 inferred conventions
- runtime inventory
- architecture map
- dependency direction notes
- important quality attributes

한 hot file이 전체 repository intent를 정의하게 하지 않는다.

## Worklist

우선순위:

- architecture boundaries and dependency direction
- runtime entrypoints
- public API and SDK surfaces
- migrations and schema boundaries
- cross-service contracts and async handoffs
- high-churn modules
- modules with many importers
- shared utilities and framework adapters
- background jobs and async consumers
- performance-sensitive paths
- low-test critical workflows

finding이 없어도 reviewed surface를 기록한다.

## Coverage Ledger

reviewed surface마다 coverage ledger row를 사용한다.

```text
| Surface | Risk Area | Evidence | Outcome | Notes |
| --- | --- | --- | --- | --- |
```

Outcome:

- `reported`
- `rejected`
- `no_issue_found`
- `not_applicable`
- `deferred`

중요 scoped surface에 row가 없고 deferred reason도 없으면 coverage는 incomplete다.

## Repo Finding Rules

- grep hit count를 coverage로 보지 않는다.
- dramatic candidate 하나에 전체 리뷰를 소모하지 않는다. 다른 high-impact surface도 확인한다.
- independently fixable repeated problematic instance는 보존한다.
- broad architecture complaint보다 concrete entrypoint/control/sink evidence를 선호한다.
- maintainability finding은 concrete change amplification 또는 inconsistency cost를 보여줘야 한다.

## Hard Rules

`references/shared-hard-rules.md`를 읽고 적용한다.
