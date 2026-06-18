"""Render a wibaek review markdown report as a self-contained HTML file."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from urllib.parse import urlsplit

DEFAULT_TEMPLATE = (
    Path(__file__).resolve().parents[1] / "assets" / "report_template.html"
)
REQUIRED_TEMPLATE_TOKENS = ("{escaped_title}", "{toc_items}", "{report_body}")


def slugify(text: str, used: set[str]) -> str:
    raw = re.sub(r"<[^>]+>", "", text).strip().lower()
    raw = re.sub(r"`([^`]+)`", r"\1", raw)
    chars = [ch if ch.isalnum() else "-" for ch in raw]
    slug = re.sub(r"-+", "-", "".join(chars)).strip("-") or "section"
    if slug not in used:
        used.add(slug)
        return slug

    index = 2
    while f"{slug}-{index}" in used:
        index += 1
    unique = f"{slug}-{index}"
    used.add(unique)
    return unique


def sanitize_href(href: str) -> str:
    decoded = html.unescape(href).strip()
    decoded = "".join(ch for ch in decoded if ch >= " " and ch != "\x7f")
    parsed = urlsplit(decoded)
    if parsed.scheme and parsed.scheme.lower() not in {
        "file",
        "http",
        "https",
        "mailto",
    }:
        return "#"
    return html.escape(decoded, quote=True)


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: (
            f'<a href="{sanitize_href(match.group(2))}">{match.group(1)}</a>'
        ),
        escaped,
    )
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def render_table(lines: list[str]) -> str:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    header: list[str] = []
    body = rows
    if len(rows) >= 2 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
        header = rows[0]
        body = rows[2:]

    output = ["<table>"]
    if header:
        output.append("<thead><tr>")
        output.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
        output.append("</tr></thead>")
    output.append("<tbody>")
    for row in body:
        output.append("<tr>")
        output.extend(f"<td>{inline_markdown(cell)}</td>" for cell in row)
        output.append("</tr>")
    output.append("</tbody></table>")
    return "\n".join(output)


def render_markdown(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    body: list[str] = []
    toc: list[tuple[int, str, str]] = []
    used_slugs: set[str] = set()
    lines = markdown.splitlines()
    index = 0
    in_code = False
    code_lines: list[str] = []

    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            if in_code:
                code = html.escape("\n".join(code_lines))
                body.append(f"<pre><code>{code}</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            index += 1
            continue

        if in_code:
            code_lines.append(line)
            index += 1
            continue

        if line.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].startswith("|"):
                table_lines.append(lines[index])
                index += 1
            body.append(render_table(table_lines))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            anchor = slugify(title, used_slugs)
            toc.append((level, title, anchor))
            body.append(f'<h{level} id="{anchor}">{inline_markdown(title)}</h{level}>')
        elif line.startswith("- "):
            items = []
            while index < len(lines) and lines[index].startswith("- "):
                items.append(lines[index][2:])
                index += 1
            body.append(
                "<ul>"
                + "".join(f"<li>{inline_markdown(item)}</li>" for item in items)
                + "</ul>"
            )
            continue
        elif re.match(r"^\d+\. ", line):
            items = []
            while index < len(lines) and re.match(r"^\d+\. ", lines[index]):
                items.append(re.sub(r"^\d+\. ", "", lines[index]))
                index += 1
            body.append(
                "<ol>"
                + "".join(f"<li>{inline_markdown(item)}</li>" for item in items)
                + "</ol>"
            )
            continue
        elif not line.strip():
            body.append("")
        else:
            body.append(f"<p>{inline_markdown(line)}</p>")
        index += 1

    if in_code:
        code = html.escape("\n".join(code_lines))
        body.append(f"<pre><code>{code}</code></pre>")

    return "\n".join(body), toc


def read_template(template_path: Path) -> str:
    template = template_path.read_text(encoding="utf-8")
    missing = [token for token in REQUIRED_TEMPLATE_TOKENS if token not in template]
    if missing:
        missing_tokens = ", ".join(missing)
        raise ValueError(f"report template is missing tokens: {missing_tokens}")
    return template


def render_page(title: str, markdown: str, template_path: Path) -> str:
    body, toc = render_markdown(markdown)
    toc_items = "\n".join(
        (
            f'<li class="toc-item depth-{level}">'
            f'<a href="#{anchor}">{inline_markdown(text)}</a></li>'
        )
        for level, text, anchor in toc
        if level <= 3
    )
    return (
        read_template(template_path)
        .replace("{escaped_title}", html.escape(title))
        .replace("{toc_items}", toc_items)
        .replace("{report_body}", body)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a wibaek review report to HTML.")
    parser.add_argument("--report-md", required=True)
    parser.add_argument("--report-html", required=True)
    parser.add_argument("--title", default="Engineering Review")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    args = parser.parse_args()

    report_md = Path(args.report_md)
    report_html = Path(args.report_html)
    markdown = report_md.read_text(encoding="utf-8")
    report_html.parent.mkdir(parents=True, exist_ok=True)
    report_html.write_text(
        render_page(args.title, markdown, Path(args.template)),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
