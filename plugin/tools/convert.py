"""Format conversion via pandoc (pypandoc-binary bundles it). Run inside the uv env.

  convert.py to-md <in.docx|in.tex|...> <out.md>      import for editing (out must be inside jobs/)
  convert.py to-docx <in.md> <out.docx> [--ref <original.docx>]
      export; --ref reuses the original's styles so the revised docx looks like the original.
      out must be inside jobs/ or named *.revised.docx; never an existing non-.revised file.
The original docx is never overwritten: the writer exports <name>.revised.docx next to it.
These checks matter because this script is allow-listed (runs without a permission prompt),
so it must not become a way to write arbitrary files around the guard hook.
"""

import os
import sys
from pathlib import Path

import pypandoc

HOME = Path(os.environ.get("WRITING_HOME", Path(__file__).resolve().parents[2])).resolve()
JOBS = HOME / "jobs"


def inside_jobs(p: Path) -> bool:
    try:
        p.relative_to(JOBS)
        return True
    except ValueError:
        return False


def main() -> None:
    cmd, src, dst, *rest = sys.argv[1:]
    out = Path(dst).expanduser().resolve()
    if cmd == "to-md":
        if not inside_jobs(out):
            sys.exit(f"refused: to-md output must be inside {JOBS}")
        pypandoc.convert_file(src, "gfm", outputfile=str(out), extra_args=["--wrap=none"])
    elif cmd == "to-docx":
        if not (inside_jobs(out) or out.name.endswith(".revised.docx")):
            sys.exit("refused: to-docx output must be inside jobs/ or named <name>.revised.docx")
        extra = ["--reference-doc", rest[1]] if rest[:1] == ["--ref"] else []
        pypandoc.convert_file(src, "docx", outputfile=str(out), extra_args=extra)
    else:
        sys.exit(__doc__)
    print(out)


if __name__ == "__main__":
    main()
