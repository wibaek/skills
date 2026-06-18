# 공유 리뷰 hard rule

mode별 guidance보다 먼저 이 규칙을 적용한다.

- workflow별 단계 경계를 보이게 유지한다. diff scan은 diff target, supporting context, evidence check, final review로 충분하다. repository/scoped scan과 deep review는 baseline, discovery, validation, impact analysis, final report 경계를 유지한다.
- repository/scoped scan과 deep review entrypoint는 goal tool이 사용 가능할 때 Codex goal을 만들거나 채택해야 하며, 관련 worklist, candidate, coverage, final report receipt가 닫히기 전에 complete하면 안 된다. diff scan mode는 goal을 사용하지 않는다.
- finding을 내기 전에 diff evidence, repository evidence, design authority 중 해당하는 근거를 확인한다.
- discovery candidate를 validated finding처럼 제시하지 않는다.
- validation evidence와 구체적 failure path 없이 P0/P1을 부여하지 않는다.
- style, naming, preference comment는 입증된 maintainability, correctness, compatibility, operational impact가 없으면 `Info`로 취급하거나 생략한다.
- 개인 취향보다 repository convention을 우선한다.
- declared intent와 inferred convention을 분리한다. 현재 majority pattern을 무조건 정답으로 만들지 않는다.
- finding을 확정하기 전에 가장 강한 counterevidence를 찾는다.
- 독립적으로 고칠 수 있는 instance를 보존한다. fix가 다르면 sibling problem을 대표 finding 하나로 숨기지 않는다.
- diff review를 unrelated repo-wide review로 넓히지 않는다.
- worklist 또는 coverage ledger 없이 broad coverage를 주장하지 않는다.
- candidate가 rejected 또는 deferred면 관련 ledger나 reviewed surface summary에 reason을 visible하게 남긴다.
- 사용자가 finding 수정을 명시적으로 요청하지 않는 한 review 중 repository file을 수정하지 않는다.

## anti-noise rule

- "조금 더 깔끔할 수 있음"은 finding이 아니다.
- "다른 abstraction이 더 취향에 맞음"은 finding이 아니다.
- "언젠가 문제가 될 수도 있음"은 현재 code에서 cost 또는 failure로 가는 plausible path가 없으면 finding이 아니다.
- nit를 blocker로 부풀리지 않는다.
- 같은 low-impact style issue를 모든 instance에 반복 comment하지 않는다.
- prototype, draft, spike, WIP 작업에서는 issue가 irreversible decision, public contract, migration, production safety에 영향을 주지 않는 한 noise floor를 낮춘다.

## evidence rule

evidence가 될 수 있는 것:

- build, test, typecheck, linter, profiler, query plan, dependency graph, import graph의 command output
- entrypoint에서 broken invariant 또는 sink까지의 source trace
- repository documentation, ADR, AGENTS.md, README, API schema, migration rule, test name
- de-facto convention을 보여주는 prevalence measurement
- precondition과 counterevidence가 포함된 concrete failure scenario

이 중 아무것도 없으면 그 항목은 finding이 아니라 suggestion에 속한다.
