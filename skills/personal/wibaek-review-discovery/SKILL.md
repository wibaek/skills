---
name: wibaek-review-discovery
description: Internal phase only for wibaek review workflows. Do not use as a top-level review entrypoint. Discovers evidence-backed engineering review candidates from a baseline and worklist.
---

# Review Discovery

후보 finding만 찾는다. 이 단계는 최종 priority, 최종 confidence, 최종 reportability를 소유하지 않는다.

## Discovery Checklist

- 실제 파일 또는 문서 evidence를 본 뒤 후보를 만든다.
- commit message, PR title, 문서의 주장보다 실제 diff/code/doc structure를 신뢰한다.
- candidate는 broken invariant 또는 concrete risk path를 가져야 한다.
- source, root control, impact sink가 다르면 후보를 나눈다.
- 같은 category라는 이유만으로 다른 instance를 합치지 않는다.
- style preference는 후보가 아니다.
- 가까운 반대 증거를 함께 적는다.
- validation plan을 같이 남긴다.

## Candidate Families

찾을 수 있는 후보 family:

- business logic, edge case, state transition
- transaction boundary, idempotency, concurrency
- API contract, schema evolution, backward compatibility
- data ownership, migration risk, isolation risk
- N+1, unbounded memory, inefficient algorithm, excessive I/O
- timeout, retry storm, partial failure, missing backpressure
- logging, metrics, tracing, alerting gaps
- missing regression test, weak contract test, overmocking, flaky test risk
- layering violation, dependency cycle, bounded-context leak, god service
- duplication, high complexity, unclear ownership, excessive abstraction

## Output Contract

각 후보는 `references/candidate-schema.md`의 canonical schema를 따른다.

필수:

- candidate id
- category
- title
- authority basis
- falsifiability
- affected locations
- invariant
- claim
- evidence
- counterevidence to check
- validation plan
- initial priority
- confidence

후보를 emit하면 candidate ledger에 discovery receipt를 남긴다. 작은 리뷰에서는 final report 내부에 discovery evidence를 보존해도 된다.

## Hard Rules

`references/shared-hard-rules.md`를 읽고 적용한다.

- discovery를 validation으로 바꾸지 않는다.
- "좋은 설계가 아님"은 finding이 아니다. 어떤 invariant가 깨지는지 말한다.
- P0/P1을 확정하지 않는다. initial priority는 provisional이다.
- candidate coverage를 암묵적으로 남기지 않는다.
