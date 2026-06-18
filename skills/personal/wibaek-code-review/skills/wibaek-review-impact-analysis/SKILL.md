---
name: wibaek-review-impact-analysis
description: Internal phase only for wibaek review workflows. Do not use as a top-level review entrypoint. Calibrates priority and confidence from failure path, blast radius, counterevidence, irreversibility, and leverage.
---

# Impact Analysis

검증된 candidate를 priority가 보정된 review finding으로 바꾼다.

## Failure Path

Info가 아닌 finding에는 경로가 필요하다.

```text
trigger/source
  -> broken invariant
  -> affected component
  -> failure mode
  -> user/product/team/cost impact
  -> counterevidence
  -> final priority
```

## Calibration Factors

각 요소를 따로 평가한다.

- correctness or reliability consequence
- blast radius and centrality
- user-visible impact
- production likelihood
- cost impact
- operational detectability and recoverability
- migration or rollback safety
- public API or data contract exposure
- leverage: whether fixing now is much cheaper than later
- counterevidence strength

## Irreversibility

되돌리기 어려운 결정은 더 엄격하게 본다.

High irreversibility:

- DB schema and historical data shape
- public API, event schema, SDK contract
- cross-service protocol
- shared abstraction with many expected consumers
- deployment/rollback strategy

Low irreversibility:

- internal leaf implementation
- isolated UI detail
- private helper with few callers
- reversible config default behind feature flag

## Priority Calibration

`../../references/authority-and-priority-policy.md`를 먼저 적용한다.

- path가 validated, central, irreversible, likely하면 올린다.
- path가 speculative, isolated, reversible, mitigated면 낮춘다.
- counterevidence가 claim을 무너뜨리면 suppress한다.
- 수사적으로 강해 보인다는 이유로 priority를 올리지 않는다.

## Output Contract

각 surviving candidate에 다음을 쓴다.

- final priority
- confidence
- failure path
- affected workflow
- blast radius
- counterevidence
- why the priority is not higher
- why the priority is not lower
- minimal remediation direction
