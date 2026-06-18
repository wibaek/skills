# 권위 근거 및 우선순위 정책

이 문서는 noise를 줄이기 위한 핵심 정책이다. 리뷰 항목이 finding이 되려면 먼저 authority basis와 falsifiability class를 가져야 한다.

## authority basis

적용 가능한 가장 강한 근거를 사용한다.

| Basis | 의미 | priority 영향 |
| --- | --- | --- |
| `machine_evidence` | 실패 테스트, build error, type error, benchmark, query plan, import graph, profiler output | impact에 따라 P0-P2까지 뒷받침 가능 |
| `declared_invariant` | AGENTS.md, ADR, README, API schema, type contract, migration rule, test name, 명시적 product rule | impact에 따라 P0-P2까지 뒷받침 가능 |
| `de_facto_convention` | repository prevalence가 실질적 contract를 보여줌. 예: 52개 module 중 47개가 boundary를 지킴 | concrete impact가 없으면 보통 P2 이하 |
| `internal_inconsistency` | 외부 규칙이 없어도 code나 docs가 자기모순을 보임 | blast radius에 따라 보통 P1-P3 |
| `named_principle` | reference 또는 common practice의 일반 engineering principle | 보통 P2-P3까지만 가능 |
| `preference` | concrete impact 없는 reviewer 취향 | finding이 아님. Info로 두거나 생략 |

## falsifiability class

| Class | receipt type | 예시 |
| --- | --- | --- |
| `machine_verifiable` | command output 또는 deterministic artifact | failing test, typecheck, import cycle, query plan, benchmark |
| `behavioral_argument` | source trace plus scenario, precondition, counterevidence | transaction split, partial failure, missing retry boundary |
| `normative` | 명시적으로 위반된 invariant 또는 수용된 team rule | layer rule, ADR consequence, documented convention |

machine-verifiable 항목은 command output이 claim을 증명하면 discovery와 validation을 합칠 수 있다. normative 항목은 authority checking을 건너뛰면 안 된다.

## priority 단계

### P0

즉시 release blocker로 취급한다.

- data loss 또는 irreversible corruption
- core workflow의 hard outage
- irreversible migration failure
- auth, billing, core workflow break
- rollback 불가능 또는 unsafe deployment risk

P0에는 강한 evidence와 concrete failure path가 필요하다. design preference에는 P0를 쓰지 않는다.

### P1

강한 수정 권고이며 보통 merge 전에 처리한다.

- production incident 가능성이 높음
- API 또는 data contract breaking change
- transaction 또는 data consistency bug
- retry storm, queue amplification, runaway cost
- important path의 심각한 performance regression
- operator가 안전하게 감지하거나 복구할 수 없는 failure
- public 또는 widely reused 상태가 되기 직전인 high-leverage bad abstraction

P1에는 validation evidence와 impact path가 필요하다.

### P2

수정을 권장한다. release context에 따라 follow-up으로 남길 수 있다.

- 특정 조건에서 발생하는 correctness issue
- localized performance 또는 reliability risk
- 의미 있는 migration 또는 compatibility risk
- regression risk를 실질적으로 높이는 test gap
- plausible failure debugging을 막는 observability gap
- future change를 헷갈리게 할 가능성이 높은 inconsistent pattern

### P3

개선 제안이다.

- local scope의 maintainability issue
- 작은 duplication
- concrete readability cost가 있는 naming 또는 structure issue
- minor docs 또는 test improvement
- low-risk refactor suggestion

### Info

blocking하지 않는 note다.

- style preference
- alternative idea
- 불명확한 future-proofing
- 취향 기반 abstraction suggestion
- behavioral impact 없는 docs wording

## priority 하한 및 상한

- `preference`는 `Info`를 넘을 수 없다.
- repository-specific evidence 없는 `named_principle`은 `P3`를 넘을 수 없다.
- failure path 없는 `de_facto_convention`은 보통 `P2`를 넘을 수 없다.
- declared invariant 없는 `normative` 항목은 `P3`를 넘을 수 없다.
- P1/P0에는 `machine_evidence`, `declared_invariant`, 또는 concrete impact가 있는 강한 `behavioral_argument`가 필요하다.
- "this is not clean"만 말하는 finding은 invalid다.

## leverage 및 irreversibility

되돌리기 어렵거나 곧 load-bearing이 될 변경은 priority를 올린다.

신호:

- public API 또는 SDK surface
- database schema 또는 migration
- event schema 또는 external contract
- 많은 module이 import하는 shared abstraction
- future caller를 끌어들일 가능성이 높은 새 module boundary
- 나쁜 pattern이 곧 복사될 high-churn area
- deployment 또는 rollback path

priority를 낮추는 경우:

- 중요한 consumer가 없는 leaf code
- prototype, spike, draft, throwaway experiment
- rollback이 쉬운 two-way-door decision
- issue가 이미 test 또는 feature flag로 격리됨

## counterevidence pass

최종 priority를 정하기 전에 묻는다.

- 이 동작이 의도된 것이고 문서화되어 있는가?
- 기존 compensating control이 있는가?
- test가 우려한 path가 불가능함을 증명하는가?
- affected path가 normal runtime에서 unreachable인가?
- broken invariant가 아니라 local style difference인가?
- 제안된 수정이 issue보다 더 큰 risk를 만드는가?

counterevidence가 강하면 suppress하거나 downgrade한다.
