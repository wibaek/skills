# 리뷰 artifact 경로

사용자가 다른 경로를 명시하지 않으면 리뷰 산출물은 임시 디렉터리에 둔다.

`/tmp`는 임시 리뷰 artifact용이다. 사용자가 영구 보존 report를 요청하면 사용자 제공 경로를 우선하고, 별도 경로가 없으면 `<repo_root>/.codex/reviews/<scan_id>/` 아래에 쓴다.

## 기본 경로

- `repo_name=<basename of repo_root>`
- `review_dir=/tmp/wibaek-review/<repo_name>/<scan_id>`
- `artifacts_dir=<review_dir>/artifacts`
- `context_dir=<artifacts_dir>/01_context`
- `worklist_dir=<artifacts_dir>/02_worklist`
- `discovery_dir=<artifacts_dir>/03_discovery`
- `reconciliation_dir=<artifacts_dir>/04_reconciliation`
- `findings_dir=<artifacts_dir>/05_findings`
- `coverage_dir=<artifacts_dir>/06_coverage`

`scan_id`는 `<commit>_<timestamp>` 형식을 선호한다. Git commit을 알 수 없으면 `local_<timestamp>`를 사용한다.

## context artifact

- project baseline: `<context_dir>/review_baseline.md`
- declared intent: `<context_dir>/declared_intent.md`
- inferred conventions: `<context_dir>/inferred_conventions.md`
- architecture map: `<context_dir>/architecture_map.md`
- runtime inventory: `<context_dir>/runtime_inventory.md`
- dependency map: `<context_dir>/dependency_map.md`

## worklist artifact

- changed or scoped input: `<worklist_dir>/rank_input.csv`
- review worklist: `<worklist_dir>/review_worklist.csv`
- deep review input: `<worklist_dir>/deep_review_input.csv`
- reviewed file receipts: `<worklist_dir>/reviewed_files.jsonl`

## discovery artifact

- discovery report: `<discovery_dir>/review_discovery_report.md`
- raw candidates: `<discovery_dir>/raw_candidates.jsonl`
- work ledger: `<discovery_dir>/work_ledger.jsonl`

## reconciliation artifact

- dedupe report: `<reconciliation_dir>/dedupe_report.md`
- deduped candidates: `<reconciliation_dir>/deduped_candidates.jsonl`
- canonical candidate inventory: `<reconciliation_dir>/canonical_candidate_inventory.md`

## finding artifact

- per-finding directory: `<findings_dir>/<candidate_id>/`
- candidate ledger: `<findings_dir>/<candidate_id>/candidate_ledger.jsonl`
- validation report: `<findings_dir>/<candidate_id>/validation_report.md`
- validation artifacts: `<findings_dir>/<candidate_id>/validation_artifacts/`
- impact analysis report: `<findings_dir>/<candidate_id>/impact_analysis_report.md`

candidate ledger receipt에는 phase, method, evidence, disposition, artifact reference를 기록한다.

## coverage artifact

- repository coverage ledger: `<coverage_dir>/repository_coverage_ledger.md`
- reviewed surfaces summary: `<coverage_dir>/reviewed_surfaces.md`

coverage artifact는 finding 목록이 아니다. reported, rejected, not applicable, deferred로 확인한 surface를 기록한다.

## 최종 output

- primary HTML report: `<review_dir>/report.html`
- markdown report source: `<review_dir>/report.md`
- report validation notes: `<review_dir>/report_validation.md`

`report.html`이 사람이 읽는 기본 entry point다. final response에는 HTML path를 먼저 쓰고,
markdown source path를 보조로 쓴다.

## report generation

`wibaek-review-final-report` skill directory를 `<skill_dir>`라고 할 때 기본 pipeline은 다음 순서다.

```bash
uv run python <skill_dir>/scripts/validate_review_report.py --report-md <review_dir>/report.md
uv run python <skill_dir>/scripts/render_review_report_html.py --report-md <review_dir>/report.md --report-html <review_dir>/report.html --title "<repo_or_target> Engineering Review"
```

검증 또는 렌더링이 실패하면 실패 output을 `<review_dir>/report_validation.md`에 기록한다.
artifact 생성을 완료하지 못했으면 final response에서 HTML report가 없다고 명확히 말한다.
