"""Write guard for the writing agent.

Two hook events:
  UserPromptSubmit (`guard.py --prompt`): records approvals that only the USER can grant, derived from
      the text the user typed (`--apply-ok`, `/writing:ingest-source`). Stored in HOME/.approvals/,
      which the agent may never write to. Approval therefore cannot be forged by the agent, or by a
      prompt injection inside a document it is editing.
  PreToolUse on Edit|Write|MultiEdit|NotebookEdit (default): decides allow / ask / deny per path.

Promises enforced:
  1. The user's own files are never modified without approval (work happens in jobs/).
  2. Skills/agents change only with explicit permission; memory/ is freely editable.
  3. Approval state (job manifests, .approvals/) is not agent-writable without the user's consent.

Only acts inside writer sessions (agent_type "writing:…"); other Claude sessions are untouched.
Stdlib only; runs with plain python3.
"""

import hashlib
import json
import os
import re
import shlex
import sys
import time
from pathlib import Path

HOME = Path(os.environ.get("CLAUDE_PLUGIN_OPTION_HOME_DIR")
            or os.environ.get("WRITING_HOME")
            or Path(__file__).resolve().parents[2]).resolve()
JOBS, MEMORY, VAULT = HOME / "jobs", HOME / "memory", HOME / "vault"
SKILLS, AGENTS, HOOKS = HOME / "plugin" / "skills", HOME / "plugin" / "agents", HOME / "plugin" / "hooks"
APPROVALS = HOME / ".approvals"
APPROVAL_TTL = 12 * 3600  # a grant from a prompt lasts for the working session, not forever


def under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def is_writer_session(event: dict) -> bool:
    return str(event.get("agent_type", "")).startswith("writing:")


# ---------- approvals: written only from the user's own prompt ----------

def grants(session_id: str | None) -> dict:
    if not session_id:
        return {}
    f = APPROVALS / f"{session_id}.json"
    try:
        g = json.loads(f.read_text())
    except (OSError, ValueError):
        return {}
    now = time.time()
    out = {k: v for k, v in g.items() if isinstance(v, (int, float)) and now - v < APPROVAL_TTL}
    if "apply_ok" in out:
        out["targets"] = [str(x) for x in g.get("targets", [])]
    return out


def _command_targets(first_line: str, cwd: str) -> list[str]:
    """Files named on the user's /writing:edit|write line: the first positional arg and any --out."""
    try:
        toks = shlex.split(first_line)
    except ValueError:
        toks = first_line.split()
    found, positional_seen = [], False
    for i, tok in enumerate(toks[1:], 1):
        if tok == "--out" and i + 1 < len(toks):
            found.append(toks[i + 1])
        elif not tok.startswith("-") and not positional_seen and toks[i - 1] != "--out":
            positional_seen = True
            found.append(tok)
    return [str((Path(cwd) / Path(f).expanduser()).resolve()) for f in found]


def record_prompt(event: dict) -> None:
    prompt, sid = str(event.get("prompt", "")), event.get("session_id")
    if not sid:
        return
    new = {}
    first_line = prompt.lstrip().split("\n", 1)[0]
    # Only the first line of a /writing: command counts, so text pasted below it can't grant anything.
    if re.match(r"\s*/writing:(?:edit|write|apply)\b[^\n]*(?<![\w-])--apply-ok\b", prompt):
        new["apply_ok"] = time.time()
        new["targets"] = _command_targets(first_line, event.get("cwd", "."))
    if re.match(r"\s*/writing:ingest-source\b", prompt):
        new["ingest"] = time.time()
    if not new:
        return
    APPROVALS.mkdir(exist_ok=True)
    f = APPROVALS / f"{sid}.json"
    old = grants(sid)
    if "targets" in new:
        new["targets"] = sorted(set(old.get("targets", [])) | set(new["targets"]))
    f.write_text(json.dumps({**old, **new}))
    for old in APPROVALS.glob("*.json"):  # prune stale grants
        if time.time() - old.stat().st_mtime > 7 * 86400:
            old.unlink(missing_ok=True)


# ---------- pre-approved apply targets ----------

def _front(mf: Path) -> dict:
    return dict(re.findall(r"^(\w+):\s*(.*)$", mf.read_text().split("\n---", 2)[0], re.M))


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def preapproved_targets(session_id: str | None) -> set[Path]:
    """Targets the user pre-approved: requires an --apply-ok grant from the user's prompt in THIS
    session, a job created after that grant, and a target still identical to its snapshot
    (or, for a new file, still nonexistent)."""
    g = grants(session_id)
    granted, allowed = g.get("apply_ok"), {Path(x) for x in g.get("targets", [])}
    if not granted:
        return set()
    out = set()
    for mf in JOBS.glob("*/manifest.md"):
        m = _front(mf)
        if m.get("apply") != "preapproved" or m.get("status") == "applied":
            continue
        try:
            created = time.mktime(time.strptime(m.get("created", ""), "%Y-%m-%dT%H:%M:%S"))
        except ValueError:
            continue
        if created < granted - 5:
            continue
        target, snap = Path(m.get("target", "")).resolve(), m.get("snapshot_sha256", "")
        if target not in allowed:  # the grant names specific files; other jobs don't inherit it
            continue
        if snap == "-" and not target.exists():
            out.add(target)
        elif target.is_file() and snap == _sha(target):
            out.add(target)
    return out


def decide(path: Path, session_id: str | None = None) -> tuple[str, str]:
    """Return (decision, reason). Policy (smoothest experience that keeps the promises):
      .approvals/ → deny · hooks/ → deny · job manifests & ingest marker → ask
      jobs/, memory/ → allow · skills/, agents/ → ask · vault/ → allow only with an ingest grant
      pre-approved target (and its <stem>.revised<ext> sibling) → allow · everything else → ask
    """
    if under(path, APPROVALS):
        return "deny", "approvals can only come from your own prompt, never from the agent"
    if under(path, HOOKS):
        return "deny", "the writer may not modify its own guard; edit plugin/hooks/ yourself"
    if under(path, JOBS) and (path.name.lower() == "manifest.md" or path.name.startswith(".")):
        return "ask", "job manifests hold approval state (target, apply mode); confirm this change"
    if under(path, JOBS) or under(path, MEMORY):
        return "allow", "writer workspace / user memory"
    if under(path, SKILLS) or under(path, AGENTS):
        return "ask", "this changes the writer's skills/agents, which needs your explicit permission"
    if under(path, VAULT):
        if grants(session_id).get("ingest"):
            return "allow", "vault write during /writing:ingest-source"
        return "ask", "vault knowledge change outside an ingest"
    for target in preapproved_targets(session_id):
        if path == target or path == target.with_name(f"{target.stem}.revised{target.suffix}"):
            return "allow", f"pre-approved (--apply-ok) apply for {target.name}"
    if under(path, HOME):
        return "ask", "change to the writing agent's own files (outside jobs/ and memory/)"
    return "ask", "this writes to YOUR file outside the job workspace; apply only if you approve the change"


def decide_bash(cmd: str) -> tuple[str, str] | None:
    """Defense in depth for shell commands in writer sessions: the file guard only sees Edit/Write,
    so block shell routes to the approval state and the guard itself. None = no opinion."""
    low = cmd.lower()
    if ".approvals" in low:
        return "deny", "shell access to approval state is not allowed; approvals come from your prompt"
    if "plugin/hooks" in low:
        return "deny", "the writer may not touch its own guard from the shell"
    if "manifest.md" in low or ".ingest" in low:
        return "ask", "this shell command touches job approval state (manifest); confirm it"
    return None


def main() -> None:
    event = json.load(sys.stdin)
    if event.get("tool_name") == "Bash":
        if is_writer_session(event):
            verdict = decide_bash(str(event.get("tool_input", {}).get("command", "")))
            if verdict:
                print(json.dumps({"hookSpecificOutput": {
                    "hookEventName": "PreToolUse", "permissionDecision": verdict[0],
                    "permissionDecisionReason": f"[writing guard] {verdict[1]}"}}))
        return
    if "--prompt" in sys.argv:
        try:
            record_prompt(event)
        except OSError:
            pass  # never block the user's prompt
        return
    if os.environ.get("WRITING_GUARD_DEBUG"):
        with open(JOBS / ".guard-debug.log", "a") as log:
            log.write(json.dumps({k: event.get(k) for k in
                                  ("session_id", "agent_type", "agent_id", "tool_name", "cwd")}) + "\n")
    if not is_writer_session(event):
        return
    ti = event.get("tool_input", {})
    raw = ti.get("file_path") or ti.get("notebook_path")
    if not raw:
        return
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path(event.get("cwd", ".")) / path
    try:
        decision, reason = decide(path.resolve(), event.get("session_id"))
    except Exception as e:  # fail CLOSED: a crashing hook would otherwise let the write through
        decision, reason = "ask", f"guard could not decide ({type(e).__name__}: {e}); confirm manually"
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": f"[writing guard] {reason}",
    }}))


if __name__ == "__main__":
    main()
