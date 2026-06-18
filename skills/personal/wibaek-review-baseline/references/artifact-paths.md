# 리뷰 artifact 경로

사용자가 다른 경로를 명시하지 않으면 리뷰 산출물은 임시 디렉터리에 둔다.

`/tmp`는 임시 리뷰 artifact용이다. 사용자가 영구 보존 report를 요청하면 사용자 제공 경로를 우선하고, 별도 경로가 없으면 `<repo_root>/.codex/reviews/<scan_id>/` 아래에 쓴다.

## 기본 경로

- `repo_name=<basename of repo_root>`
- `review_dir=/tmp/wibaek-code-review/<repo_name>/<scan_id>`
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

- markdown report: `<review_dir>/report.md`
- optional HTML report: `<review_dir>/report.html`
- report validation notes: `<review_dir>/report_validation.md`
