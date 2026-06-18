# 리뷰 candidate schema

discovery, validation, merge, final report 전반에서 하나의 canonical candidate shape를 사용한다.

```json
{
  "candidate_id": "CR-001",
  "category": "transaction-boundary",
  "title": "결제 실패 처리 전에 주문 생성이 재고를 예약할 수 있음",
  "authority_basis": "declared_invariant",
  "falsifiability": "behavioral_argument",
  "affected_locations": [
    {
      "label": "entrypoint",
      "path": "src/orders/api.py",
      "lines": "42-68",
      "detail": "주문 생성을 위한 HTTP entrypoint"
    },
    {
      "label": "root_control",
      "path": "src/orders/service.py",
      "lines": "101-138",
      "detail": "재고 변경과 결제 호출이 rollback boundary 밖으로 분리되어 있음"
    },
    {
      "label": "impact_sink",
      "path": "src/payments/client.py",
      "lines": "77-94",
      "detail": "remote payment call은 재고 변경 이후 실패할 수 있음"
    }
  ],
  "invariant": "partial failure 이후 order, payment, inventory state가 갈라지면 안 된다.",
  "claim": "재고 예약 이후 결제가 실패하면 결제 가능한 주문 없이 재고가 잠길 수 있다.",
  "evidence": [
    "src/orders/service.py:118에서 payment client 호출 전에 재고를 예약한다",
    "error를 반환하기 전에 rollback 또는 compensation path가 보이지 않는다"
  ],
  "counterevidence_to_check": [
    "payment failure 이후 inventory reservation을 해제하는 reconciliation job이 있을 수 있다"
  ],
  "validation_plan": [
    "기존 order failure test 실행",
    "transaction rollback behavior 추적",
    "inventory reconciliation job 검색"
  ],
  "initial_priority": "P1",
  "confidence": "medium"
}
```

## 필수 field

- `candidate_id`: `CR-001` 같은 stable id.
- `category`: 정규화된 review category 하나.
- `title`: concrete issue title.
- `authority_basis`: 이것을 문제라고 부를 수 있는 근거.
- `falsifiability`: claim을 확인할 수 있는 방식.
- `affected_locations`: object array. string-only location은 금지한다.
- `invariant`: 깨진 rule 또는 expected property.
- `claim`: candidate finding을 한 문장으로 요약한 것.
- `evidence`: 이미 관찰한 repository evidence.
- `counterevidence_to_check`: finding에 반대되는 가장 강할 가능성이 있는 evidence.
- `validation_plan`: confirm 또는 reject를 위한 bounded check.
- `initial_priority`: impact analysis 전 provisional priority.
- `confidence`: provisional confidence.

## affected location label

label은 일관되게 사용한다.

- `entrypoint`: request, job, CLI, API, hook, public method, document section.
- `root_control`: invariant가 잘못 enforce되거나 enforce되지 않는 line.
- `impact_sink`: side effect, external call, persistence, contract, migration, expensive operation.
- `concrete_implementation`: broad claim을 concrete하게 만드는 subclass, route, handler, migration, strategy, consumer.
- `test_gap`: finding이 regression coverage에 관한 경우 test file 또는 missing test boundary.
- `doc_section`: design doc, ADR, RFC, README section.

## category set

아래 category에서 시작하고, 필요할 때만 추가한다.

- `business-logic`
- `edge-case`
- `state-transition`
- `transaction-boundary`
- `idempotency`
- `concurrency`
- `time-handling`
- `numeric-precision`
- `layering-violation`
- `dependency-cycle`
- `bounded-context-leak`
- `wrong-abstraction`
- `god-service`
- `data-ownership`
- `module-coupling`
- `breaking-change`
- `error-contract`
- `pagination`
- `schema-evolution`
- `migration-risk`
- `missing-index`
- `isolation-risk`
- `query-fanout`
- `n-plus-one`
- `unbounded-memory`
- `inefficient-algorithm`
- `cache-stampede`
- `missing-timeout`
- `retry-storm`
- `partial-failure`
- `missing-backpressure`
- `logging-gap`
- `metrics-gap`
- `tracing-gap`
- `missing-regression-test`
- `weak-contract-test`
- `overmocking`
- `flaky-test-risk`
- `duplication`
- `high-complexity`
- `unclear-ownership`
- `dead-code`
- `inconsistent-pattern`
- `excessive-abstraction`
