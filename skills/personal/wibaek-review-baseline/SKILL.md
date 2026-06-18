---
name: wibaek-review-baseline
description: Internal phase only for wibaek review workflows. Do not use as a top-level review entrypoint. Restores declared intent, conventions, architecture/runtime context, quality priorities, and review invariants.
---

# Review Baseline

보안 스캔의 threat model에 해당한다. 리뷰가 취향 기반으로 흐르지 않도록 저장소 또는 문서의 의도와 기준을 먼저 복원한다.

## Objective

다음 정보를 확보한다.

- declared intent: AGENTS.md, README, ADR, docs, API contract, test names에 명시된 기준
- inferred conventions: 코드에서 반복적으로 드러난 사실상 관례와 prevalence
- architecture/runtime context: entrypoint, module boundary, dependency direction, data ownership
- quality priorities: correctness, reliability, performance, maintainability, operability, compatibility, cost
- review invariants: 이번 리뷰에서 finding을 판단할 기준

## Workflow

1. 사용자 요청의 target과 review mode를 확인한다.
2. 저장소 지침, README, ADR, docs, package/build metadata를 읽는다.
3. target에 필요한 범위에서 runtime entrypoint와 module boundary를 매핑한다.
4. declared intent와 inferred conventions를 분리해서 기록한다.
5. inferred convention은 prevalence를 가능하면 수치로 적는다. 예: "47/52 service가 domain -> repository 방향을 따른다."
6. declared intent와 inferred convention이 충돌하면 충돌 자체를 baseline finding 후보가 아니라 discovery input으로 남긴다.
7. baseline artifact를 `references/artifact-paths.md`의 context path에 저장하거나, 파일 산출물이 필요 없는 작은 리뷰에서는 final report의 Baseline section에 남긴다.

## Hard Rules

`references/shared-hard-rules.md`를 읽고 적용한다.

- current diff만 보고 repository intent를 정하지 않는다.
- 코드 다수가 하는 일을 자동으로 정답으로 취급하지 않는다.
- 선언된 기준과 추론된 관례를 섞지 않는다.
- baseline 단계에서 finding을 확정하지 않는다.
- 문서나 코드에 없는 기준을 개인 취향으로 만들지 않는다.
