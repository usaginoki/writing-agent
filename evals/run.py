"""Run the writer on every eval case and score each revision with a judge model.

  python3 evals/run.py [--cases 01,05] [--mode quick] [--parallel 4] [--judge-model sonnet]

For each evals/cases/NN-*.md: the "# Original" section is written to evals/runs/<ts>/NN/original.md,
the writer edits it headlessly (`/writing:edit … <mode> --trust`, never applied), and a judge scores
the job's latest version with evals/judge.md. Results: evals/runs/<ts>/results.json plus a table.
evals/runs/ is git-ignored (it contains book text).
"""

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

HOME = Path(__file__).resolve().parents[1]
CASES, JOBS = HOME / "evals" / "cases", HOME / "jobs"
TOOLS = [
    "Read", "Glob", "Grep", "Write", "Edit", "Agent", "Skill",
    # exact scripts only: a wildcard on `uv run` or tools/* would pre-approve arbitrary code/writes
    f"Bash(python3 {HOME}/plugin/tools/job.py *)", f"Bash(python3 {HOME}/plugin/tools/textstats.py *)",
    f"Bash(uv run -q --project {HOME} python {HOME}/plugin/tools/convert.py *)",
]


def section(text: str, name: str) -> str:
    m = re.search(rf"^# {name}\s*\n(.*?)(?=^# |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def find_job(target: Path) -> Path | None:
    for mf in sorted(JOBS.glob("*/manifest.md"), reverse=True):
        if f"target: {target}" in mf.read_text():
            return mf.parent
    return None


def run_case(case: Path, out: Path, mode: str, judge_model: str) -> dict:
    cid = case.name[:2]
    d = out / cid
    d.mkdir(parents=True)
    original = d / "original.md"
    original.write_text(section(case.read_text(), "Original") + "\n")
    w = subprocess.run(["claude", "-p", "--agent", "writing:writer", "--allowedTools", *TOOLS, "--",
                        f"/writing:edit {original} {mode} --trust"],
                       cwd=d, capture_output=True, text=True, timeout=1200)
    (d / "writer.log").write_text(w.stdout + w.stderr)
    job = find_job(original.resolve())
    if not job:
        return {"id": cid, "error": "no job created"}
    current = re.search(r"^current:\s*(\S+)", (job / "manifest.md").read_text(), re.M).group(1)
    revision = next(job.glob(f"{current}.*")).read_text()
    (d / "revision.md").write_text(revision)
    prompt = ((HOME / "evals" / "judge.md").read_text() + "\n\n## Case file\n" + case.read_text()
              + "\n\n## Agent revision\n" + revision + "\n\nReturn ONLY the JSON object.")
    j = subprocess.run(["claude", "-p", "--model", judge_model, "--", prompt],
                       capture_output=True, text=True, timeout=600)
    m = re.search(r"\{.*\}", j.stdout, re.S)
    try:
        verdict = json.loads(m.group(0)) if m else {"error": j.stdout[-500:]}
    except json.JSONDecodeError:
        verdict = {"error": "unparseable judge output", "raw": j.stdout[-500:]}
    return {"id": cid, "job": str(job), **verdict}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases")
    ap.add_argument("--mode", default="quick")
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--judge-model", default="sonnet")
    a = ap.parse_args()
    cases = sorted(CASES.glob("*.md"))
    if a.cases:
        keep = set(a.cases.split(","))
        cases = [c for c in cases if c.name[:2] in keep]
    out = HOME / "evals" / "runs" / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True)
    with cf.ThreadPoolExecutor(a.parallel) as ex:
        results = list(ex.map(lambda c: run_case(c, out, a.mode, a.judge_model), cases))
    (out / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    keys = ["principles", "meaning", "concision", "naturalness"]
    print(f"{'id':3} " + " ".join(f"{k[:10]:>10}" for k in keys) + "  verdict")
    for r in results:
        s = r.get("scores", {})
        print(f"{r['id']:3} " + " ".join(f"{s.get(k, '-'):>10}" for k in keys) + f"  {r.get('verdict', r.get('error', ''))[:70]}")
    ok = [r for r in results if "scores" in r]
    if ok:
        print("avg " + " ".join(f"{sum(r['scores'][k] for r in ok) / len(ok):>10.2f}" for k in keys))
    print(f"\nresults: {out / 'results.json'}")


if __name__ == "__main__":
    sys.exit(main())
