"""PreToolUse guard for the writing agent (Edit | Write | NotebookEdit).

Enforces two promises:
  1. The user's own files are never modified without approval (work happens in jobs/).
  2. Skills/agents (the agent's "code") change only with explicit permission;
     memory/ (the user's preferences) is freely editable.

Only acts inside writer sessions: the writer agent (agent_type "writing:…") or a session
that registered itself via jobs/.active/<session_id>. Any other Claude session is untouched.
Stdlib only; runs with plain python3.
"""

import json
import os
import re
import sys
from pathlib import Path

HOME = Path(os.environ.get("CLAUDE_PLUGIN_OPTION_HOME_DIR")
            or os.environ.get("WRITING_HOME")
            or Path(__file__).resolve().parents[2]).resolve()
JOBS, MEMORY, VAULT = HOME / "jobs", HOME / "memory", HOME / "vault"
SKILLS, AGENTS, HOOKS = HOME / "plugin" / "skills", HOME / "plugin" / "agents", HOME / "plugin" / "hooks"


def under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def is_writer_session(event: dict) -> bool:
    if str(event.get("agent_type", "")).startswith("writing:"):
        return True
    sid = event.get("session_id")
    return bool(sid) and (JOBS / ".active" / sid).exists()


def preapproved_targets() -> set[Path]:
    """Targets of jobs started with --apply-ok that haven't been applied yet."""
    out = set()
    for mf in JOBS.glob("*/manifest.md"):
        front = dict(re.findall(r"^(\w+):\s*(.*)$", mf.read_text().split("\n---", 2)[0], re.M))
        if front.get("apply") == "preapproved" and front.get("status") != "applied":
            out.add(Path(front.get("target", "")).resolve())
    return out


def ingest_active() -> bool:
    return (JOBS / ".ingest-active").exists()


def decide(path: Path) -> tuple[str, str]:
    """Return (decision, reason). decision is "allow", "ask" or "deny".

    TODO(user): write this policy (~10 lines). Available helpers:
      under(path, ROOT)          ROOT in JOBS, MEMORY, VAULT, SKILLS, AGENTS, HOOKS, HOME
      preapproved_targets()      set of user files the user pre-approved for this job
      ingest_active()            True while /writing:ingest-source is running
    Trade-offs to choose:
      - skills/agents: "ask" lets you approve in-session; "deny" forces you to edit them yourself.
      - hooks/ (this file): the agent editing its own guard is the riskiest write. Ask, or deny?
      - vault/ outside ingest: knowledge, not code. Allow, or ask?
      - user files: ask unless pre-approved. Should pre-approval also cover *new* files next to
        the target (e.g. report.revised.docx), or only the exact target path?
      - anything else under HOME (pyproject, tools/): ask?
    The reason string is shown in the permission prompt, so make it say *why*.

    Chosen policy (smoothest experience that keeps both promises):
      jobs/, memory/ → allow · skills/, agents/ → ask · hooks/ → deny · vault/ → allow only while ingesting
      pre-approved target (and its <stem>.revised<ext> sibling) → allow · everything else → ask
    """
    if under(path, JOBS) or under(path, MEMORY):
        return "allow", "writer workspace / user memory"
    if under(path, HOOKS):
        return "deny", "the writer may not modify its own guard; edit plugin/hooks/ yourself"
    if under(path, SKILLS) or under(path, AGENTS):
        return "ask", "this changes the writer's skills/agents, which needs your explicit permission"
    if under(path, VAULT):
        if ingest_active():
            return "allow", "vault write during /writing:ingest-source"
        return "ask", "vault knowledge change outside an ingest"
    for target in preapproved_targets():
        if path == target or path == target.with_name(f"{target.stem}.revised{target.suffix}"):
            return "allow", f"pre-approved apply for {target.name}"
    if under(path, HOME):
        return "ask", "change to the writing agent's own files (outside jobs/ and memory/)"
    return "ask", "this writes to YOUR file outside the job workspace; apply only if you approve the change"


def main() -> None:
    event = json.load(sys.stdin)
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
        decision, reason = decide(path.resolve())
    except Exception as e:  # fail CLOSED: a crashing hook would otherwise let the write through
        decision, reason = "ask", f"guard could not decide ({type(e).__name__}: {e}); confirm manually"
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": f"[writing guard] {reason}",
    }}))


if __name__ == "__main__":
    main()
