#!/usr/bin/env python3
"""Build CV.pdf from ../data.json using HTML + Chrome headless print."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parent
DATA_PATH = ROOT / "data.json"
STYLE_PATH = DIR / "style.css"
PREVIEW_PATH = DIR / "preview.html"
OUTPUT_PATH = ROOT / "CV.pdf"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

EXT_ICON = (
    '<svg class="ext" width="9" height="9" viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="currentColor" d="M14 3h7v7h-2V6.4l-9.3 9.3-1.4-1.4L17.6 5H14V3zM5 5h6v2H7v10h10v-4h2v6H5V5z"/>'
    "</svg>"
)

ICONS = {
    "email": (
        '<svg class="icon" width="11" height="11" viewBox="0 0 24 24" aria-hidden="true">'
        '<path fill="currentColor" d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/>'
        "</svg>"
    ),
    "phone": (
        '<svg class="icon" width="11" height="11" viewBox="0 0 24 24" aria-hidden="true">'
        '<path fill="currentColor" d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1.1-.3 1.2.4 2.5.6 3.8.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.6.6 3.8.1.4 0 .8-.3 1.1L6.6 10.8z"/>'
        "</svg>"
    ),
    "portfolio": (
        '<svg class="icon" width="11" height="11" viewBox="0 0 24 24" aria-hidden="true">'
        '<path fill="currentColor" d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm7 9h-1.1c-.1-1.2-.4-2.3-.8-3.3.8.9 1.5 2 1.9 3.3zM12 4.1c.9 1.2 1.6 2.7 2 4.4h-4c.4-1.7 1.1-3.2 2-4.4zM4.3 13c-.2-.6-.3-1.3-.3-2s.1-1.4.3-2h2.2c-.1.7-.1 1.3-.1 2s0 1.3.1 2H4.3zm1.6 2h1.9c.4 1.5 1 2.9 1.7 4-1.6-.8-2.9-2.2-3.6-4zM8.4 7H6.5c.7-1.8 2-3.2 3.6-4-.7 1.1-1.3 2.5-1.7 4zM12 19.9c-.9-1.2-1.6-2.7-2-4.4h4c-.4 1.7-1.1 3.2-2 4.4zM15.8 19c.7-1.1 1.3-2.5 1.7-4h1.9c-.7 1.8-2 3.2-3.6 4zM17.6 13h2.1c.2-.6.3-1.3.3-2s-.1-1.4-.3-2h-2.1c.1.7.1 1.3.1 2s0 1.3-.1 2zM17.6 7c-.4-1.5-1-2.9-1.7-4 1.6.8 2.9 2.2 3.6 4h-1.9z"/>'
        "</svg>"
    ),
    "linkedin": (
        '<svg class="icon" width="11" height="11" viewBox="0 0 24 24" aria-hidden="true">'
        '<path fill="currentColor" d="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zM8.3 18.3H5.7V9.7h2.6v8.6zM7 8.4a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zM18.3 18.3h-2.6v-4.2c0-1-.4-1.7-1.4-1.7-.8 0-1.2.5-1.4 1-.1.2-.1.5-.1.8v4.1h-2.6s.0-6.6 0-7.3h2.6v1c.3-.6 1-1.4 2.5-1.4 1.8 0 3.2 1.2 3.2 3.7v4z"/>'
        "</svg>"
    ),
    "github": (
        '<svg class="icon" width="11" height="11" viewBox="0 0 24 24" aria-hidden="true">'
        '<path fill="currentColor" d="M12 2C6.5 2 2 6.5 2 12c0 4.4 2.9 8.2 6.8 9.5.5.1.7-.2.7-.5v-1.7c-2.8.6-3.4-1.2-3.4-1.2-.4-1.1-1.1-1.4-1.1-1.4-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.5 2.3 1.1 2.9.8.1-.6.3-1.1.6-1.3-2.2-.2-4.6-1.1-4.6-5 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.7 1a9.4 9.4 0 0 1 5 0c1.9-1.3 2.7-1 2.7-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.9-2.3 4.7-4.6 5 .4.3.7.9.7 1.8v2.7c0 .3.2.6.7.5C19.1 20.2 22 16.4 22 12c0-5.5-4.5-10-10-10z"/>'
        "</svg>"
    ),
}


def md_to_html(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", escaped)
    return escaped


def linkify_bold(text_html: str, links: list[dict] | None) -> str:
    if not links:
        return text_html
    result = text_html
    for link in links:
        label = html.escape(link["label"])
        url = html.escape(link["url"], quote=True)
        needle = f"<strong>{label}</strong>"
        if needle in result:
            result = result.replace(
                needle,
                f'<a class="inline-link" href="{url}" target="_blank"><strong>{label}</strong>{EXT_ICON}</a>',
                1,
            )
    return result


def bullet_html(bullet) -> str:
    if isinstance(bullet, dict):
        body = linkify_bold(md_to_html(bullet["text"]), bullet.get("links"))
    else:
        body = md_to_html(bullet)
    return f"<li>{body}</li>"


def bullets_html(bullets: list) -> str:
    if not bullets:
        return ""
    return f'<ul class="bullets">{"".join(bullet_html(b) for b in bullets)}</ul>'


def title_with_link(title: str, url: str | None) -> str:
    title_h = html.escape(title)
    if not url:
        return f'<span class="entry-title">{title_h}</span>'
    href = html.escape(url, quote=True)
    return (
        f'<a class="title-link" href="{href}" target="_blank">{title_h}{EXT_ICON}</a>'
    )


def build_html(data: dict) -> str:
    style = STYLE_PATH.read_text(encoding="utf-8")

    contact_html = "".join(
        f'<a class="contact-item" href="{html.escape(item["url"], quote=True)}">'
        f'{ICONS.get(item["type"], "")}<span>{html.escape(item["label"])}</span></a>'
        for item in data["contact"]
    )

    exp_parts = []
    for job in data["experience"]:
        company = html.escape(job["company"])
        if job.get("companyUrl"):
            href = html.escape(job["companyUrl"], quote=True)
            company_h = (
                f'<div><a class="entry-sub" href="{href}" target="_blank">'
                f"{company}{EXT_ICON}</a></div>"
            )
        else:
            company_h = f'<div class="entry-sub">{company}</div>'
        exp_parts.append(
            f"""
            <article class="entry">
              <div class="entry-head">
                <div class="entry-title">{html.escape(job["title"])}</div>
                <div class="entry-dates">{html.escape(job["dates"])}</div>
              </div>
              {company_h}
              <div class="entry-desc">{md_to_html(job["description"])}</div>
              {bullets_html(job["bullets"])}
            </article>
            """
        )

    def include_on_cv(item: dict) -> bool:
        return item.get("cv", True) is not False

    project_parts = [
        f"""
        <article class="entry">
          <div>{title_with_link(proj['title'], proj.get('url'))}</div>
          <div class="entry-desc">{md_to_html(proj['description'])}</div>
          {bullets_html(proj['bullets'])}
        </article>
        """
        for proj in data["projects"]
        if include_on_cv(proj)
    ]

    edu_parts = [
        f"""
        <article class="entry keep">
          <div class="edu-row">
            <div class="entry-title">{html.escape(edu["degree"])}</div>
            <div class="entry-dates">{html.escape(edu["dates"])}</div>
          </div>
          <div class="edu-meta">
            <em>{html.escape(edu["school"])}</em>
            <span>{html.escape(edu["location"])}</span>
          </div>
          <div class="edu-detail">{html.escape(edu["detail"])}</div>
        </article>
        """
        for edu in data["education"]
    ]

    skill_parts = []
    for skill in data["skills"]:
        items = skill["items"]
        if isinstance(items, list):
            names = ", ".join(
                item["name"] if isinstance(item, dict) else str(item) for item in items
            )
        else:
            names = str(items)
        skill_parts.append(
            f"<li><strong>{html.escape(skill['category'])}</strong> — {html.escape(names)}</li>"
        )

    awards = [a for a in data["awards"] if include_on_cv(a)]
    cols = [[], [], []]
    for i, award in enumerate(awards):
        cols[i % 3].append(award)

    def award_cell(award: dict) -> str:
        title = html.escape(award["title"])
        if award.get("url"):
            href = html.escape(award["url"], quote=True)
            return (
                f'<a class="award" href="{href}" target="_blank">{title}{EXT_ICON}</a>'
            )
        return f'<div class="award">{title}</div>'

    award_cells = []
    for i in range(max((len(c) for c in cols), default=0)):
        for col in cols:
            award_cells.append(award_cell(col[i]) if i < len(col) else '<div class="award"></div>')

    lead_items = [item for item in (data.get("leadership") or []) if include_on_cv(item)]
    lead_parts = [
        f"""
        <article class="entry keep">
          <div class="entry-head">
            <div class="entry-title">{html.escape(item["organization"])}</div>
            <div class="entry-dates">{html.escape(item["dates"])}</div>
          </div>
          <div class="entry-sub">{html.escape(item["role"])}</div>
          {bullets_html(item["bullets"])}
        </article>
        """
        for item in lead_items
    ]
    leadership_section = (
        f"""
    <section class="section">
      <h2 class="section-title">Leadership &amp; Extracurriculars</h2>
      {"".join(lead_parts)}
    </section>
"""
        if lead_items
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{html.escape(data["name"])} Resume</title>
  <style>{style}</style>
</head>
<body>
  <main class="cv">
    <header class="header">
      <h1 class="name">{html.escape(data["name"])}</h1>
      <div class="contact">{contact_html}</div>
    </header>

    <p class="summary">{md_to_html(data["summary"])}</p>

    <section class="section">
      <h2 class="section-title">Work Experience</h2>
      {"".join(exp_parts)}
    </section>

    <section class="section">
      <h2 class="section-title">Academic Projects</h2>
      {"".join(project_parts)}
    </section>

    <section class="section">
      <h2 class="section-title">Education</h2>
      {"".join(edu_parts)}
    </section>

    <section class="section">
      <h2 class="section-title">Skills</h2>
      <ul class="skills-list">{"".join(skill_parts)}</ul>
    </section>

    <section class="section section-awards">
      <h2 class="section-title">Awards and Certifications</h2>
      <div class="awards">{"".join(award_cells)}</div>
    </section>
    {leadership_section}
  </main>
</body>
</html>
"""


def print_pdf(html_path: Path, pdf_path: Path) -> None:
    if not Path(CHROME).exists():
        raise SystemExit(f"Google Chrome not found at {CHROME}")

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not pdf_path.exists():
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(f"Chrome failed to print PDF (exit {result.returncode})")


def stamp_page_numbers(pdf_path: Path) -> None:
    """Add FlowCV-style 'n / N' page numbers using PyMuPDF."""
    script = f"""
import fitz
from pathlib import Path
pdf_path = Path({str(pdf_path)!r})
doc = fitz.open(pdf_path)
n = doc.page_count
for i, page in enumerate(doc):
    r = page.rect
    text = f"{{i + 1}} / {{n}}"
    tw = fitz.get_text_length(text, fontsize=9.45, fontname="times-roman")
    page.insert_text(
        (r.width / 2 - tw / 2, r.height - 22),
        text,
        fontsize=9.45,
        fontname="times-roman",
        color=(0, 0, 0),
    )
tmp = pdf_path.with_suffix(".tmp.pdf")
doc.save(tmp)
doc.close()
tmp.replace(pdf_path)
"""
    candidates = [
        Path("/tmp/cv-venv/bin/python"),
        Path(sys.executable),
    ]
    for py in candidates:
        if not py.exists():
            continue
        result = subprocess.run([str(py), "-c", script], capture_output=True, text=True)
        if result.returncode == 0:
            return
    print(
        "Warning: PyMuPDF not available; PDF generated without page numbers.\n"
        "Install with: python3 -m venv /tmp/cv-venv && /tmp/cv-venv/bin/pip install pymupdf",
        file=sys.stderr,
    )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    html_doc = build_html(data)

    # Write preview beside fonts/ so @font-face relative urls resolve
    PREVIEW_PATH.write_text(html_doc, encoding="utf-8")
    print_pdf(PREVIEW_PATH, OUTPUT_PATH)
    stamp_page_numbers(OUTPUT_PATH)

    info = subprocess.check_output(["pdfinfo", str(OUTPUT_PATH)], text=True)
    pages = next(
        (line.split(":")[1].strip() for line in info.splitlines() if line.startswith("Pages:")),
        "?",
    )
    print(f"Wrote {OUTPUT_PATH} ({pages} pages)")
    print(f"Preview HTML: {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
