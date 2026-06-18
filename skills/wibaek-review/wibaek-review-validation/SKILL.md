---
name: wibaek-review-validation
description: Internal phase only for wibaek review workflows. Do not use as a top-level review entrypoint. Validates or rejects discovered review candidates with tests, traces, typechecks, graphs, or scenario evidence.
---

# Review Validation

후보 finding을 가능한 가장 강한 evidence로 검증하거나 반증한다.

## Workflow

1. 각 candidate의 falsifiability class를 확인한다.
2. feasible하고 비례적인 가장 강한 validation method를 선택한다.
3. 필요한 command, test, trace, graph, scenario walkthrough를 실행하거나 수행한다.
4. counterevidence를 명시적으로 찾는다.
5. disposition을 `confirmed`, `rejected`, `deferred` 중 하나로 정한다.
6. validation receipt를 candidate ledger에 남긴다.

## Method Examples

- correctness bug: focused unit/integration test
- transaction bug: rollback test, failure injection, static transaction trace
- API compatibility: contract test, generated client compile, schema diff
- migration risk: dry-run, lock/backfill analysis, backward compatibility check
- performance: benchmark, query count, EXPLAIN plan, profiler
- architecture boundary: import graph, dependency graph, public API consumer trace
- concurrency: race reproducer, lock ordering trace, idempotency check
- observability: failure scenario and log/metric/trace inspection
- maintainability: concrete change amplification example and repository convention evidence
- design doc: failure-mode walkthrough and decision reversibility analysis

## Hard Rules

- validation이 일어나지 않았는데 일어난 것처럼 말하지 않는다.
- feasible한 stronger evidence가 있으면 weaker argument에서 멈추지 않는다.
- setup error를 즉시 반증으로 취급하지 않는다.
- rejected/deferred reason을 정확히 남긴다.
- P1/P0 후보는 validation evidence 없이는 `wibaek-review-impact-analysis`로 올리지 않는다.
