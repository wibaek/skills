# design doc 및 ADR review

architecture proposal, RFC, ADR, design doc, system design writeup에 사용한다.

## review 형태

1. problem framing을 추출한다.
2. goal, non-goal, constraint, invariant를 추출한다.
3. proposed architecture, data flow, runtime flow, rollout을 매핑한다.
4. candidate risk를 발견한다.
5. failure-mode walkthrough로 risk를 검증한다.
6. impact와 reversibility를 분석한다.
7. ADR-style feedback 또는 review comment를 만든다.

## finding 기준

모든 design finding에는 concrete scenario가 필요하다.

```text
trigger
  -> design assumption 또는 missing decision
  -> failure mode
  -> affected user/system/team
  -> impact
  -> counterevidence in the doc
```

모호한 concern은 finding이 아니다.

나쁜 예:

- "Caching이 어려울 수 있음."
- "Kafka가 복잡해 보임."
- "scaling을 생각해야 함."

좋은 예:

- "deploy 시 모든 worker가 cache warmup 없이 cold-start하며, primary DB에 대한 estimated read QPS가 5k에서 50k로 뛴다. proposal에는 load shedding, cache warmup, fallback이 없어 rollout 중 cascading read failure가 날 수 있다."

## decision reversibility

major decision을 분류한다.

- `one_way`: 되돌리기 어렵다. 예: data model, public API, event schema, consistency model, storage engine.
- `two_way`: 되돌리기 싸다. 예: internal helper shape, feature flag default, isolated UI flow.

weakly justified one-way decision에 review 에너지를 쓴다. impact path가 concrete하지 않으면 two-way decision은 block하지 않는다.

## checklist

- problem이 명확히 제시되어 있다.
- non-goal이 명시되어 있다.
- constraint가 latency, cost, migration, team skill, operation을 포함한다.
- alternative가 단순 나열이 아니라 비교되어 있다.
- data flow와 read/write path가 concrete하다.
- failure mode가 partial failure, retry, rollback, overload를 포함한다.
- migration이 rollout, backfill, rollback을 포함한다.
- operability가 metric, log, alert, runbook need를 포함한다.
- cost driver가 명명되어 있다.
- relevant할 때 security와 tenant boundary가 최소한 언급되어 있다.
- test 및 validation strategy가 있다.
- consequence가 decision과 일치한다.

## ADR-specific output

ADR review에는 다음을 포함한다.

- summary
- missing context
- decision quality
- alternative 및 tradeoff
- consequence
- follow-up implication
- accept 전 필요한 change
- 유용할 때 suggested ADR patch
