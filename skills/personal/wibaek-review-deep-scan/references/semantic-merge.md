# semantic merge 및 deep review

6개 subagent lane이 candidate list를 만들 때 사용한다.

## 코드 리뷰 기본값

security deep scan은 recall을 최대화하기 위해 candidate를 union하는 경우가 많다. 일반 code review는 noise amplifier가 되지 않도록 해야 한다.

기본 merge policy:

- consensus를 사용해 confidence를 높인다.
- outlier는 automatic finding이 아니라 더 엄격한 validation 대상 candidate로 사용한다.
- 다른 evidence가 뒷받침하지 않는 candidate는 suppress하거나 downgrade한다.
- authority basis와 validation evidence가 강할 때만 single-worker finding을 보존한다.

## merge 가능 조건

하나의 fix가 모든 upstream candidate를 해결할 때만 candidate를 merge한다.

merge 허용 예:

- "Signup API가 대소문자만 다른 중복 email을 허용함"
- "User creation에서 email normalization이 빠짐"

두 candidate가 같은 root control을 가리키고 하나의 normalization fix로 둘 다 닫히면 merge한다.

merge 금지 예:

- "Signup API에 idempotency가 없음"
- "Payment webhook에 idempotency가 없음"

category는 같지만 source/control/impact/fix가 다르다. 별도로 유지한다.

## merge record

다음을 기록한다.

- canonical candidate id
- upstream candidate id 목록
- merge rationale
- 각 upstream candidate에서 보존한 evidence
- strengthened 또는 weakened된 field
- counterevidence
- rejected된 upstream candidate가 있는지 여부

## outlier 처리

worker 하나에서만 나온 candidate도 다음 조건이면 살아남을 수 있다.

- machine evidence가 확인함
- declared invariant가 명확히 위반됨
- failure path가 concrete하고 counterevidence가 약함

그렇지 않으면 `needs_validation` 또는 `rejected_as_noise`로 표시한다.

## six-subagent fanout

deep review는 다음 6개 lane의 서로 다른 brief를 사용한다.

- correctness and data flow
- architecture boundaries and dependency direction
- API, schema, and external contract
- data model, migration, and state consistency
- performance, reliability, and operability
- testing, maintainability, and change risk

six-subagent fanout을 사용할 때:

- 각 candidate에 source lane을 표시한다.
- title 또는 category만으로 lane 간 candidate를 merge하지 않는다.
- 같은 candidate schema를 요구한다.
- merge 이후 validation과 priority calibration을 중앙에서 수행한다.
