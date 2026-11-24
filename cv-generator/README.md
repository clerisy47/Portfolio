# CV Generator

Rebuilds the FlowCV-style resume as `CV.pdf` from [`../data.json`](../data.json).

Uses HTML + CSS (Amiri font, accent `#348aa7`) printed through Chrome headless, then stamps page numbers with PyMuPDF.

## Requirements

- Google Chrome (macOS)
- Python 3
- PyMuPDF for page numbers (optional but recommended):

```bash
python3 -m venv /tmp/cv-venv
/tmp/cv-venv/bin/pip install pymupdf
```

## Usage

```bash
python3 cv-generator/generate.py
```

Outputs:

- `CV.pdf` at the repo root
- `cv-generator/preview.html` for browser preview

Edit `data.json` to change content. Use `**bold**` for emphasis; optional `url` fields become clickable links.

The same `data.json` also feeds the portfolio website. CV generation only uses the resume fields (`summary`, `experience`, `projects`, `education`, `skills`, `awards`, `leadership`, `contact`). Website-only fields like `portfolio`, `stats`, and `social` are ignored here.
