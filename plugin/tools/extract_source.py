"""Extract a PDF source into per-section markdown files for vault ingestion.

Usage:
    uv run --project $WRITING_HOME plugin/tools/extract_source.py <pdf> <sections.json> <out_dir>

sections.json: [{"id": "L03", "title": "Actions", "start": 42, "end": 59}, ...]
Pages are 1-based PDF page numbers, inclusive. Each section is written to
<out_dir>/<id> <title>.md with a header recording its page range, so notes can
cite pages. pymupdf4llm keeps italics/bold, which matter for before/after examples.
"""

import json
import sys
from pathlib import Path

import pymupdf4llm


def main() -> None:
    pdf, spec, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    for s in json.loads(spec.read_text()):
        pages = list(range(s["start"] - 1, s["end"]))  # pymupdf4llm is 0-based
        md = pymupdf4llm.to_markdown(pdf, pages=pages, show_progress=False)
        header = f"<!-- source pdf pages {s['start']}-{s['end']} ; book pages {s.get('book', '?')} -->\n\n"
        path = out / f"{s['id']} {s['title']}.md"
        path.write_text(header + md)
        print(f"{path.name}: {len(md.split())} words")


if __name__ == "__main__":
    main()
