"""Validate the required structure of a wibaek review markdown report."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = (
    "## 범위",
    "## Baseline",
    "## Review Receipt",
    "## Architecture / System Design Review",
    "## findings 요약",
    "## reviewed surfaces",
)
REQUIRED_FINDING_FIELDS = (
    "우선순위",
    "신뢰도",
    "Category",
    "Authority",
    "Validation",
)
REQUIRED_FINDING_SUBSECTIONS = (
    "#### 요약",
    "#### Evidence",
    "#### Validation",
    "#### Impact Path",
    "#### Counterevidence",
    "#### Recommendation",
    "#### 최소 수정",
    "#### 테스트 계획",
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
FINDING_RE = re.compile(r"^### \[(?:A?\d+|Info-\d+)\]\s+(.+?)\s*$", re.MULTILINE)
FIELD_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$", re.MULTILINE)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def top_level_headings(text: str) -> list[tuple[str, int]]:
    return [
        (match.group(0), match.start())
        for match in HEADING_RE.finditer(text)
        if match.group(1) in {"#", "##"}
    ]


def validate_required_sections(text: str, errors: list[str]) -> None:
    headings = top_level_headings(text)
    if not headings or not headings[0][0].startswith("# 엔지니어링 리뷰:"):
        errors.append("line 1: report must start with '# 엔지니어링 리뷰: <target>'")

    positions: list[int] = []
    for section in REQUIRED_SECTIONS:
        match = re.search(rf"^{re.escape(section)}\s*$", text, re.MULTILINE)
        if not match:
            errors.append(f"required section is missing: {section}")
            continue
        positions.append(match.start())

    if len(positions) == len(REQUIRED_SECTIONS) and positions != sorted(positions):
        errors.append("required sections are not in the expected order")


def finding_body(
    text: str,
    finding: re.Match[str],
    next_finding: re.Match[str] | None,
) -> str:
    start = finding.end()
    end = next_finding.start() if next_finding else len(text)
    return text[start:end]


def validate_finding_metadata(body: str, line: int, errors: list[str]) -> None:
    first_subsection = body.find("\n#### ")
    metadata = body[: first_subsection if first_subsection != -1 else len(body)]
    fields = {
        match.group(1).strip().rstrip(":") for match in FIELD_ROW_RE.finditer(metadata)
    }
    missing = [field for field in REQUIRED_FINDING_FIELDS if field not in fields]
    if missing:
        errors.append(
            f"line {line}: finding metadata is missing fields: {', '.join(missing)}"
        )

    if "Affected lines" not in fields and "Affected surfaces" not in fields:
        errors.append(
            f"line {line}: finding metadata needs Affected lines or Affected surfaces"
        )


def validate_finding_subsections(body: str, line: int, errors: list[str]) -> None:
    positions: list[int] = []
    for subsection in REQUIRED_FINDING_SUBSECTIONS:
        match = re.search(rf"^{re.escape(subsection)}\s*$", body, re.MULTILINE)
        if not match:
            errors.append(f"line {line}: finding is missing subsection: {subsection}")
            continue
        positions.append(match.start())
    if len(positions) == len(REQUIRED_FINDING_SUBSECTIONS) and positions != sorted(positions):
        errors.append(f"line {line}: finding subsections are not in the expected order")


def validate_findings(text: str, errors: list[str]) -> None:
    findings = list(FINDING_RE.finditer(text))
    if not findings:
        if not re.search(r"^###?\s+No findings\s*$", text, re.IGNORECASE | re.MULTILINE):
            errors.append("report needs at least one finding entry or a No findings section")
        return

    for index, finding in enumerate(findings):
        line = line_number(text, finding.start())
        body = finding_body(
            text,
            finding,
            findings[index + 1] if index + 1 < len(findings) else None,
        )
        validate_finding_metadata(body, line, errors)
        validate_finding_subsections(body, line, errors)


def validate_report(text: str) -> list[str]:
    errors: list[str] = []
    validate_required_sections(text, errors)
    validate_findings(text, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a wibaek review report.")
    parser.add_argument("--report-md", required=True)
    args = parser.parse_args()

    report_path = Path(args.report_md)
    errors = validate_report(report_path.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"report format validation passed: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
