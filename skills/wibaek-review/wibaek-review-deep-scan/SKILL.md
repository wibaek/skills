---
name: wibaek-review-deep-scan
description: Run wibaek-review-scan plus six explicit subagents for deep engineering review. Use when the user explicitly asks for deep, exhaustive, multi-perspective, multi-agent, or high-confidence review.
---

# Review Deep Scan

`wibaek-review-scan`을 기준으로 전체 코드, 시스템 디자인, 아키텍처 디자인을 리뷰한 뒤,
명시적 subagent 6개를 호출해 관점별 누락을 줄이는 deep review에 사용한다.
최종 report format은 `wibaek-review-scan`과 동일하다.

## When To Use

- "깊게 리뷰해줘"
- "여러 관점으로 다시 봐줘"
- "놓친 거 없게 봐줘"
- repository-wide high-confidence review
- false positive를 엄격히 거르고 싶은 scoped module review
- consensus가 confidence를 실질적으로 높이는 design 또는 architecture review

사용자가 depth를 명시적으로 요청하지 않는 빠른 PR feedback에는 사용하지 않는다.

## Goal Setup

실질적인 deep review 작업 전에 `references/goal-setup.md`의 `wibaek-review-deep-scan` objective로 Codex goal을 생성하거나 호환되는 active goal을 이어받는다.

goal을 완료하려면 6개 subagent lane의 output 또는 capability blocker가 기록되어야 하고,
canonical candidate는 validation 및 impact analysis receipt 또는 rejected/deferred reason을 가져야 하며,
final report가 작성 또는 final response에 포함되어야 한다.

## Workflow

1. `wibaek-review-scan` 규칙으로 target scope, baseline, worklist를 만든다.
2. 같은 baseline과 worklist를 6개 subagent에 명시적으로 전달한다.
3. subagent output은 raw candidate로만 보존하고 즉시 finding으로 승격하지 않는다.
4. `references/semantic-merge.md`로 raw candidate를 canonical candidate set으로 병합한다.
5. canonical candidate set을 `wibaek-review-validation`으로 중앙 검증한다.
6. `wibaek-review-impact-analysis`와 `references/authority-and-priority-policy.md`로 priority를 중앙 보정한다.
7. `wibaek-review-final-report`로 normal final report를 작성한다.

## Required Subagents

가능하면 multi-agent 또는 subagent tool로 정확히 6개 subagent를 명시적으로 호출한다.
각 subagent는 동일한 target, baseline, worklist를 받고 자신에게 배정된 관점의 candidate만 낸다.

1. system architecture, module boundaries, and dependency direction
2. domain model, data ownership, lifecycle invariant, and state consistency
3. integration architecture: API, schema, external contract, event, job, batch, CLI
4. correctness, edge case, and request/data flow
5. performance, reliability, operability, migration, and rollback
6. testing strategy, maintainability, change risk, and abstraction fit

1-3번 lane은 line-local bug보다 architecture/system design 후보를 먼저 찾아야 한다.
4-6번 lane도 code finding만 내지 말고 자신이 본 architecture surface의 outcome을 적는다.

subagent tool을 사용할 수 없으면 deep review라고 주장하지 않는다.
사용자에게 capability 부재를 말하고 ordinary `wibaek-review-scan`으로 fallback할지 확인한다.

## Deep Review Policy

일반 엔지니어링 리뷰는 worker concern을 전부 union하면 노이즈 증폭기가 된다.

- subagent 간 agreement로 confidence를 올린다.
- 약한 one-off concern은 `needs_validation`, `Info`, rejected noise로 처리한다.
- machine-verifiable evidence 또는 explicit authority basis가 강한 one-off finding만 보존한다.
- final report shape는 normal review와 동일하게 유지한다.

## Merge Rules

Subagent output은 discovery input일 뿐이다.
validation과 priority calibration은 중앙에서 수행한다.
같은 root cause는 하나의 canonical candidate로 합치고,
source, control, impact, fix가 다르면 별도 candidate로 유지한다.

## Hard Rules

`references/shared-hard-rules.md`를 읽고 적용한다.
