# 리뷰 validation 가이드

validation은 candidate의 falsifiability class에 맞는 엄격도로 candidate를 증명하거나 반증한다.

## validation ladder

feasible하고 proportional하면 더 강한 evidence를 선호한다.

1. focused failing test 또는 reproduction.
2. existing test, build, lint, typecheck, contract check, migration dry-run.
3. deterministic analysis: import graph, dependency graph, query plan, benchmark, profiler, schema diff.
4. entrypoint에서 broken invariant 또는 impact sink까지의 static trace.
5. scenario, precondition, counterevidence를 포함한 behavioral argument.
6. declared invariant 또는 accepted convention에 대한 normative confirmation.

더 강한 level이 싸고 priority를 바꿀 가능성이 있으면 약한 level에서 멈추지 않는다.

## candidate별 method

| Candidate type | 선호 validation |
| --- | --- |
| correctness bug | focused unit 또는 integration test |
| transaction bug | rollback test, failure injection, static transaction trace |
| API compatibility | contract test, generated client compile, schema diff |
| migration risk | dry-run, lock/backfill analysis, backward compatibility check |
| performance | benchmark, query count, EXPLAIN plan, profiler |
| architecture boundary | import graph, dependency graph, public API consumer trace |
| concurrency | race reproducer, lock ordering trace, idempotency check |
| observability | failure scenario와 log/metric/trace inspection |
| maintainability | concrete change amplification example 및 repository convention evidence |
| design doc | failure-mode walkthrough 및 decision reversibility analysis |

## validation receipt

validation에 들어간 각 candidate에 대해 다음을 기록한다.

- candidate id
- 사용한 method
- inspect한 command 또는 file
- 관찰한 evidence
- 발견한 counterevidence
- disposition: `confirmed`, `rejected`, `deferred`
- confidence: `high`, `medium`, `low`
- proof gap, 있다면

receipt 예시:

```json
{
  "phase": "validation",
  "candidate_id": "CR-001",
  "method": "static_trace_plus_test_search",
  "evidence": [
    "Inventory is reserved before payment client call",
    "No rollback test covers payment failure after reservation"
  ],
  "counterevidence": [
    "No reconciliation job found for abandoned reservations"
  ],
  "disposition": "confirmed",
  "confidence": "medium",
  "artifact": "artifacts/05_findings/CR-001/validation_report.md"
}
```

## rejection rule

다음이면 reject 또는 downgrade한다.

- 우려한 path가 unreachable이다.
- test 또는 type/schema contract가 이미 invariant를 enforce한다.
- compensating mechanism이 존재하고 문서화되어 있다.
- issue가 local style preference다.
- proposed finding이 speculative future requirement를 필요로 한다.

## deferred rule

candidate가 여전히 plausible하지만 concrete reason 때문에 proof가 막혔을 때만 `deferred`를 사용한다.

좋은 deferred reason:

- required service를 사용할 수 없음
- migration dry-run에 local에 없는 production-like schema가 필요함
- benchmark에 representative data가 필요함
- design doc이 key decision을 생략했고 code가 아직 없음

나쁜 deferred reason:

- "needs more review"
- "probably risky"
- "not sure"
