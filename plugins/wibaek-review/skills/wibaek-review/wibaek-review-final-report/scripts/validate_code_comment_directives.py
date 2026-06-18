from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DIRECTIVE_RE = re.compile(r"::code-comment\{(?P<body>.*)\}")
QUOTED_ATTR_RE = re.compile(r"(?P<key>[A-Za-z_][A-Za-z0-9_]*)=\"(?P<value>[^\"]*)\"")
BARE_ATTR_RE = re.compile(r"(?P<key>[A-Za-z_][A-Za-z0-9_]*)=(?P<value>[^\"\s{}]+)")
REQUIRED_ATTRS = {"title", "body", "file", "start", "end", "priority"}


def parse_attrs(raw: str) -> tuple[dict[str, str], list[str]]:
    attrs: dict[str, str] = {}
    errors: list[str] = []
    position = 0

    while position < len(raw):
        while position < len(raw) and raw[position].isspace():
            position += 1
        if position >= len(raw):
            break

        quoted = QUOTED_ATTR_RE.match(raw, position)
        bare = BARE_ATTR_RE.match(raw, position)
        match = quoted or bare
        if not match:
            errors.append("invalid attribute syntax, possibly from an unescaped double quote")
            break

        attrs[match.group("key")] = match.group("value")
        position = match.end()

    return attrs, errors


def validate_directive(line: str, line_number: int) -> list[str]:
    errors: list[str] = []
    match = DIRECTIVE_RE.search(line)
    if not match:
        return errors

    attrs, parse_errors = parse_attrs(match.group("body"))
    errors.extend(f"line {line_number}: {error}" for error in parse_errors)

    missing = sorted(REQUIRED_ATTRS - attrs.keys())
    if missing:
        errors.append(f"line {line_number}: missing required attrs: {', '.join(missing)}")

    file_value = attrs.get("file")
    if file_value and not Path(file_value).is_absolute():
        errors.append(f"line {line_number}: file must be an absolute path")

    for int_attr in ("start", "end", "priority"):
        value = attrs.get(int_attr)
        if value is None:
            continue
        try:
            parsed = int(value)
        except ValueError:
            errors.append(f"line {line_number}: {int_attr} must be an integer")
            continue
        if int_attr in {"start", "end"} and parsed < 1:
            errors.append(f"line {line_number}: {int_attr} must be >= 1")
        if int_attr == "priority" and parsed not in {0, 1, 2, 3}:
            errors.append(f"line {line_number}: priority must be 0, 1, 2, or 3")

    return errors


def validate_report(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for line_number, line in enumerate(text.splitlines(), start=1):
        errors.extend(validate_directive(line, line_number))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Codex code-comment directives.")
    parser.add_argument("report", type=Path, help="Markdown report path.")
    args = parser.parse_args()

    errors = validate_report(args.report)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated code-comment directives: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
