# 리뷰 goal 설정

repository/scoped scan과 deep review entrypoint는 runtime이 goal tool을 제공할 때 Codex goal을 사용한다. diff scan mode는 goal을 사용하지 않는다.

## ownership

- `wibaek-review-scan`, `wibaek-review-deep-scan`은 goal lifecycle을 소유한다.
- `wibaek-review-diff-scan`은 goal을 만들거나 채택하지 않는다.
- `wibaek-review-baseline`, `wibaek-review-discovery`, `wibaek-review-validation`, `wibaek-review-impact-analysis`, `wibaek-review-final-report` 같은 phase skill은 별도 goal을 만들지 않는다.
- 현재 review target을 이미 포괄하는 compatible active goal이 있으면 그 goal 아래에서 계속한다.
- repository/scoped scan 또는 deep review에서 compatible active goal이 없고 goal tool이 사용 가능하면 실질적인 review 작업 전에 goal을 만든다.
- repository/scoped scan 또는 deep review에서 goal tool이 없으면 첫 visible review update에서 같은 coverage objective를 말하고 계속한다.

## objective 문구

아래 entry에 가까운 문구를 사용한다. `<resolved target>`은 구체적인 PR, commit, branch diff, path, package, module, service boundary, document, repository target으로 바꾼다.

### wibaek-review-scan

```text
<resolved target>에 대해 wibaek-code-review scan을 실행한다. 모든 in-scope file, surface, document section, worklist row가 completion receipt나 명시적 deferred closure를 갖고, 모든 candidate가 필요한 discovery, validation, impact analysis receipt를 갖고, final review report가 작성되거나 출력될 때까지 멈추지 않는다.
```

### wibaek-review-deep-scan

```text
<resolved target>에 대해 wibaek-code-review deep scan을 실행한다. wibaek-review-scan 기준의 baseline/worklist를 만들고 6개 subagent lane을 명시적으로 실행한 뒤, 모든 canonical candidate가 필요한 discovery, validation, impact analysis receipt를 갖고, final review report가 작성되거나 출력될 때까지 멈추지 않는다.
```

## completion criteria

적용 가능한 조건이 모두 true가 될 때까지 goal을 complete로 표시하지 않는다.

- 모든 worklist row, scoped surface, changed source-like file, document section이 `reported`, `rejected`, `no_issue_found`, `not_applicable`, `deferred` 중 하나로 close되어 있다.
- 모든 discovery candidate가 discovery에 대한 candidate ledger receipt를 가지고, validation plus impact analysis 또는 명시적인 deferred/rejected reason을 가진다.
- final report의 모든 finding이 candidate id, evidence, priority rationale, fix guidance로 거슬러 올라간다.
- 모든 rejected 또는 deferred candidate는 candidate ledger, coverage ledger, reviewed surface summary 중 적절한 곳에 visible reason을 가진다.
- final markdown report가 resolved output path에 쓰였거나 final response에 포함되었다.

`wibaek-review-deep-scan`에서는 completion 전에 6개 subagent lane의 output 또는 capability blocker가 기록되어야 한다.

- `subagents_complete`: 6개 lane output이 모두 수집되었다.
- `subagent_capability_blocked`: subagent tool을 사용할 수 없어 deep review를 완료할 수 없다.
- `scope_limited`: 요청 target이 available context에 비해 너무 넓고 deferred area를 나열했다.

## blocking

선택된 workflow에 subagent, external tool, credential이 필요하지만 사용할 수 없으면 가능하면 실질적인 review 작업 전에 block한다. goal 시작 후 blocker가 나타나면 goal을 open 상태로 두고 missing capability와 next action을 기록한다.
