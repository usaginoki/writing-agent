"""Job workspaces: the writer never edits a user's file in place; it works on copies here.

Usage (WRITING_HOME defaults to the repo containing this file):
  job.py new <target|-> [--mode quick|thorough] [--trust|--no-trust] [--apply ask|preapproved]
                        [--genre essay|notes|paper|other] [--slug SLUG] [--out PATH]
      --out: for new drafts, the file the result will be applied to (recorded once, at creation).
      '-' reads pasted text from stdin (no target; result is delivered, not applied).
      Prints the job dir. Creates manifest.md, original.<ext>, v0.<ext>, questions.md, decisions.md.
  job.py list                      recent jobs with status
  job.py status <job>              manifest + question counts
  job.py check <job>               is the target unchanged since the snapshot? (exit 1 if changed)
  job.py hunks <job> <a> <b>       paragraph-level hunks as JSON (for review UI / terminal review)
  job.py diff <job> <a> <b>        unified diff, also saved to diffs/<a>-<b>.diff
  job.py set <job> key=value ...   update manifest fields (status, current, applied_version …).
                                   Approval fields (apply, target, snapshot_sha256, created) are
                                   fixed at creation and cannot be changed.
<job> may be a full path or a dir name under jobs/. Versions are names like v0, v1, v2 (extension inferred).
"""

import datetime as dt
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path(os.environ.get("WRITING_HOME", Path(__file__).resolve().parents[2]))
JOBS = HOME / "jobs"
TEXT_EXT = {".md", ".markdown", ".txt", ".tex", ".rst"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_manifest(job: Path) -> dict:
    m = re.match(r"---\n(.*?)\n---", (job / "manifest.md").read_text(), re.S)
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def write_manifest(job: Path, data: dict, body: str | None = None) -> None:
    path = job / "manifest.md"
    if body is None and path.exists():
        body = path.read_text().split("\n---\n", 1)[1] if "\n---\n" in path.read_text() else ""
    front = "\n".join(f"{k}: {v}" for k, v in data.items())
    path.write_text(f"---\n{front}\n---\n{body or ''}")


def resolve(job: str) -> Path:
    p = Path(job)
    if not p.is_absolute() and not (p / "manifest.md").exists():
        p = JOBS / job
    if not (p / "manifest.md").exists():
        sys.exit(f"no job at {p}")
    return p


def version_path(job: Path, v: str) -> Path:
    hits = sorted(job.glob(f"{v}.*"))
    if not hits:
        sys.exit(f"no version {v} in {job}")
    return hits[0]


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "text"


def to_markdown_docx(src: Path, dst: Path) -> None:
    subprocess.run(["uv", "run", "-q", "--project", str(HOME), "python", str(HOME / "plugin/tools/convert.py"),
                    "to-md", str(src), str(dst)], check=True, stdout=subprocess.DEVNULL)


def cmd_new(args: list[str]) -> None:
    target = args[0]
    opts = {"mode": "thorough", "apply": "ask", "genre": "other", "slug": None, "trust": None, "out": None}
    it = iter(args[1:])
    for a in it:
        if a in ("--trust", "--no-trust"):
            opts["trust"] = a == "--trust"
        else:
            opts[a.lstrip("-")] = next(it)
    trust = opts["trust"] if opts["trust"] is not None else opts["mode"] == "quick"
    today = dt.date.today().isoformat()

    if target == "-":
        text, src, ext = sys.stdin.read(), None, ".md"
        slug = opts["slug"] or slugify(" ".join(text.split()[:5]))
    else:
        src = Path(target).expanduser().resolve()
        if not src.exists():
            sys.exit(f"target not found: {src}")
        ext = src.suffix.lower()
        slug = opts["slug"] or slugify(src.stem)

    job = JOBS / f"{today}-{slug}"
    n = 2
    while job.exists():
        job = JOBS / f"{today}-{slug}-{n}"
        n += 1
    (job / "diffs").mkdir(parents=True)
    (job / "variants").mkdir()
    (job / "feedback").mkdir()

    if src is None:
        (job / "original.md").write_text(text)
        work_ext = ".md"
    else:
        shutil.copy2(src, job / f"original{ext}")
        if ext == ".docx":
            to_markdown_docx(src, job / "v0.md")
            work_ext = None
        elif ext in TEXT_EXT:
            work_ext = ext
        else:
            sys.exit(f"unsupported format {ext}: use md/txt/tex/docx or paste text")
    if work_ext:
        shutil.copy2(job / f"original{work_ext}", job / f"v0{work_ext}")

    target, snapshot = (str(src), sha(src)) if src else ("(pasted)", "-")
    if opts["out"]:
        out = Path(opts["out"]).expanduser().resolve()
        target, snapshot = str(out), (sha(out) if out.exists() else "-")
    data = {
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "target": target,
        "format": ext.lstrip("."),
        "genre": opts["genre"],
        "mode": opts["mode"],
        "trust": str(trust).lower(),
        "apply": opts["apply"],
        "snapshot_sha256": snapshot,
        "current": "v0",
        "status": "intake",
    }
    write_manifest(job, data, "\n# Notes\n")
    (job / "intent.md").write_text(
        "# Intent\n<!-- purpose · reader · main point: the reference for meaning checks -->\n")
    (job / "questions.md").write_text(
        "# Questions\n<!-- Format per entry (heading starts at column 0):\n  ## Q<n> · open|assumed|answered · <topic>\n<question>\n"
        "- options: a) … b) …\n**Assumed:** …   (trust mode: what the agent went with)\n**Answer:** …   (you fill this in)\n-->\n")
    (job / "decisions.md").write_text("# Decisions\n<!-- revision plan and the reason for each decision -->\n")
    print(job)


def cmd_list(_args: list[str]) -> None:
    for job in sorted(JOBS.glob("*/manifest.md"), reverse=True)[:20]:
        m = read_manifest(job.parent)
        q = (job.parent / "questions.md").read_text()
        open_q = len(re.findall(r"^## Q\d+ · (?:open|assumed)", q, re.M))
        print(f"{job.parent.name:40} {m.get('status', '?'):10} {m.get('mode', '?'):9} "
              f"cur={m.get('current', '?'):4} unresolved_q={open_q}  {m.get('target')}")


def cmd_status(args: list[str]) -> None:
    job = resolve(args[0])
    m = read_manifest(job)
    q = (job / "questions.md").read_text()
    counts = {s: len(re.findall(rf"^## Q\d+ · {s}", q, re.M)) for s in ("open", "assumed", "answered")}
    versions = sorted(p.name for p in job.glob("v*.*"))
    print(json.dumps({"job": str(job), **m, "questions": counts, "versions": versions}, indent=1))


def cmd_check(args: list[str]) -> None:
    job = resolve(args[0])
    m = read_manifest(job)
    if m["target"] == "(pasted)":
        print("PASTED: nothing to check")
        return
    t = Path(m["target"])
    if not t.exists():
        print(f"MISSING: {t}")
        sys.exit(1)
    if sha(t) != m["snapshot_sha256"]:
        print(f"CHANGED: {t} was modified after the job snapshot. Re-run intake or merge manually.")
        sys.exit(1)
    print(f"OK: {t} unchanged since snapshot")


def paragraphs(text: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", text.strip())]


def cmd_hunks(args: list[str]) -> None:
    job = resolve(args[0])
    a, b = paragraphs(version_path(job, args[1]).read_text()), paragraphs(version_path(job, args[2]).read_text())
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    hunks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        hunks.append({"id": len(hunks) + 1, "kind": tag,
                      "before": "\n\n".join(a[i1:i2]), "after": "\n\n".join(b[j1:j2]),
                      "before_range": [i1 + 1, i2], "after_range": [j1 + 1, j2]})
    print(json.dumps({"from": args[1], "to": args[2], "hunks": hunks}, indent=1, ensure_ascii=False))


def cmd_diff(args: list[str]) -> None:
    job = resolve(args[0])
    pa, pb = version_path(job, args[1]), version_path(job, args[2])
    d = "".join(difflib.unified_diff(pa.read_text().splitlines(True), pb.read_text().splitlines(True),
                                     pa.name, pb.name))
    (job / "diffs" / f"{args[1]}-{args[2]}.diff").write_text(d)
    print(d)


PROTECTED = {"apply", "target", "snapshot_sha256", "created"}


def cmd_set(args: list[str]) -> None:
    job = resolve(args[0])
    m = read_manifest(job)
    for kv in args[1:]:
        k, v = kv.split("=", 1)
        if k in PROTECTED:
            sys.exit(f"refused: '{k}' is fixed at job creation (approval state); start a new job instead")
        m[k] = v
    write_manifest(job, m)
    print(json.dumps(m, indent=1))


if __name__ == "__main__":
    cmds = {"new": cmd_new, "list": cmd_list, "status": cmd_status, "check": cmd_check,
            "hunks": cmd_hunks, "diff": cmd_diff, "set": cmd_set}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]](sys.argv[2:])
