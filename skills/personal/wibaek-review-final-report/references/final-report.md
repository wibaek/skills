# 최종 리뷰 report

diff, repo, scoped, deep, architecture, design-doc review에서 하나의 report shape를 사용한다.

## report 구조

```markdown
# 엔지니어링 리뷰: <repo_or_target>

## 범위
- mode:
- target:
- reviewed surfaces:
- 실행한 command:
- 제한 사항:

## Baseline
<declared intent, inferred conventions, architecture/runtime summary>

## findings 요약

| ID | 우선순위 | 신뢰도 | Category | 제목 |
| --- | --- | --- | --- | --- |

## Findings

### [1] <title>

| Field | Value |
| --- | --- |
| 우선순위 | P1 |
| 신뢰도 | medium |
| Category | transaction-boundary |
| Authority | declared_invariant |
| Affected lines | path:line |
| Validation | static trace + focused test search |

#### 요약
#### Evidence
#### Validation
#### Impact Path
#### Counterevidence
#### Recommendation
#### 최소 수정
#### 테스트 계획

## reviewed surfaces

| Surface | Risk Area | Outcome | Notes |
| --- | --- | --- | --- |

## 열린 질문 / follow-up
```

## finding 규칙

- priority 순서로 정렬한다: P0, P1, P2, P3, Info.
- 일반 summary prose보다 finding을 먼저 둔다.
- rejected candidate를 finding으로 포함하지 않는다. 유용하면 reviewed surfaces에 둔다.
- proof gap을 명시한다.
- "code smell"이 아니라 concrete category를 사용한다.
- remediation은 최소 범위로 쓰고 broken invariant에 연결한다.

## reviewed surface outcome

- `Reported`: finding이 되었다.
- `Rejected`: plausible candidate가 evidence로 반증되었다.
- `No issue found`: review했고 credible issue가 살아남지 않았다.
- `Not applicable`: 해당 risk class가 적용되지 않는다.
- `Needs follow-up`: plausible하지만 exact proof gap 때문에 막혔다.

## Codex inline comment directive

Codex app에서 최종 comment를 반환할 때, 현재 Codex runtime이 code review directive를 지원하는 경우에만 살아남은 actionable finding마다 directive를 하나 emit한다. 지원하지 않으면 file/line reference가 있는 일반 markdown finding을 출력한다.

priority mapping:

- `P0` -> `priority=0`
- `P1` -> `priority=1`
- `P2` -> `priority=2`
- `P3` -> `priority=3`
- `Info` -> 사용자가 모든 note를 요청한 경우가 아니면 보통 directive를 만들지 않는다.

format:

```text
::code-comment{title="[P1] 결제 실패 후 재고 예약이 남을 수 있음" body="주문 경로는 결제 호출 전에 재고를 예약하지만 결제가 실패할 때 rollback 또는 compensation이 보이지 않는다. 결제 가능한 주문 없이 재고가 unavailable 상태로 남을 수 있으므로 transaction boundary 또는 compensation path를 추가하고 결제 실패 동작을 regression test로 덮어라." file="/absolute/path/src/orders/service.py" start=101 end=138 priority=1 confidence=0.65}
```

directive 규칙:

- `title`, `body`, `file`, `start`, `end`, `priority`는 필수다.
- `file`은 absolute path여야 한다.
- line range는 가장 좁은 root cause line을 가리켜야 한다.
- emit 전에 quoted attribute value 안의 double quote를 escape하거나 제거한다.
- report와 directive의 title, priority, file, explanation은 일치해야 한다.

directive가 포함된 markdown report를 disk에 쓰면, script가 사용 가능할 때 `scripts/validate_code_comment_directives.py`로 directive syntax를 검증한다.
