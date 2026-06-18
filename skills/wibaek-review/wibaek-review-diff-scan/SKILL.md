---
name: wibaek-review-diff-scan
description: Lightweight review for Git diffs, PRs, commits, branch diffs, staged changes, or working-tree patches. Use for ordinary PR feedback focused on changed code, not repository-wide or architecture reviews.
---

# Review Diff Scan

PR, commit, branch diff, staged changes, unstaged changes, working-tree patch를 단순 리뷰한다.
목표는 changed code에서 바로 고칠 수 있는 correctness, contract, test, maintainability risk를 찾고,
필요한 경우 리뷰 품질을 위해 supporting context만 조금 더 보는 것이다.

## Lightweight Phase

1. diff target을 확정한다.
2. changed file과 changed line을 먼저 읽는다.
3. 변경 의도를 이해하는 데 필요한 supporting file만 조금 추가한다.
4. 의심 항목을 evidence와 counterevidence로 빠르게 확인한다.
5. actionable finding과 짧은 summary를 final response로 낸다.

formal baseline, discovery, validation, impact-analysis artifact를 만들지 않는다.
필요한 판단 근거는 final response 안에 inline으로 보존한다.

## Scope Rules

- 시작 전에 정확한 diff target을 해석한다.
- review 대상은 changed source-like file과 changed line이 기본이다.
- changed source-like file은 모두 한 번 이상 훑는다.
- changed behavior를 이해하는 데 필요한 supporting file만 추가한다.
- unrelated repository-wide review로 넓히지 않는다.
- PR title, commit message보다 actual diff를 신뢰한다.

## Supporting Files

다음에 해당할 때만 supporting file을 추가한다.

- 직접 호출되는 service/helper/schema/model
- 변경된 API contract consumer
- 변경된 migration model 또는 rollback path
- 기대 동작을 정의하는 test
- shared helper 변경이 영향을 줄 수 있는 caller
- 변경된 runtime behavior를 제어하는 config/deploy file

근처에 있다는 이유만으로 supporting file을 추가하지 않는다.

## Sibling Coverage

diff가 재사용 패턴을 바꾸고, 확인 비용이 낮을 때만 sibling instance를 따라간다.

- shared helper
- route pattern
- serializer/deserializer
- query builder
- migration template
- public API schema
- job/queue handler
- transaction helper
- cache invalidation helper

source, control, sink, fix가 다르면 sibling instance를 별도 finding으로 둘 수 있지만,
ordinary diff review에서는 changed behavior와 직접 연결된 항목을 우선한다.

## Diff Finding Rules

- finding은 diff와 overlap하거나 diff 때문에 새로 reachable해야 한다.
- 기존 문제가 diff와 무관하면 사용자가 더 넓은 리뷰를 요청하지 않는 한 reviewed context에만 남긴다.
- inline PR comment는 broken control이 changed line이면 changed line에 단다. 아니라면 가장 가까운 root-cause line에 달고 diff와의 관계를 설명한다.
- public contract가 바뀌면 feasible한 범위에서 consumer 또는 generated type을 확인한다.

## Commands To Consider

repository guidance를 먼저 따른다. 일반적으로 고려할 명령:

- `git diff --stat`
- `git diff --name-only`
- focused `git diff` for changed files
- relevant unit/integration tests
- lint, format check, typecheck
- migration이 바뀐 경우 migration dry-run
- API가 바뀐 경우 generated client 또는 schema compatibility check

## Hard Rules

`references/shared-hard-rules.md`를 읽고 적용한다.
