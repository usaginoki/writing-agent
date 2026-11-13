"""Branch and attack tests for guard.py. Run: python3 plugin/hooks/test_guard.py

Encodes the agreed policy. Approvals must come from the user's own prompt (UserPromptSubmit),
never from agent-writable state; the "attack" cases check that forging that state doesn't work.
"""

import datetime as dt
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

GUARD = Path(__file__).with_name("guard.py")


def hook(home: Path, event: dict, *args: str) -> str:
    return subprocess.run([sys.executable, str(GUARD), *args], input=json.dumps(event), text=True,
                          capture_output=True, env={"WRITING_HOME": str(home), "PATH": "/usr/bin:/bin"}).stdout.strip()


def write(home: Path, path, sid="S", agent_type: str | None = "writing:writer") -> str:
    event = {"session_id": sid, "tool_name": "Write", "cwd": str(home), "tool_input": {"file_path": str(path)}}
    if agent_type:
        event["agent_type"] = agent_type
    out = hook(home, event)
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "(none)"


def prompt(home: Path, text: str, sid="S", cwd: Path | None = None) -> None:
    hook(home, {"session_id": sid, "prompt": text, "cwd": str(cwd or home),
                "hook_event_name": "UserPromptSubmit"}, "--prompt")


def manifest(home: Path, name: str, target: Path, apply: str, created: dt.datetime, snap: str | None = None):
    d = home / "jobs" / name
    d.mkdir(parents=True)
    if snap is None:
        snap = hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else "-"
    (d / "manifest.md").write_text(f"---\ncreated: {created.isoformat(timespec='seconds')}\ntarget: {target}\n"
                                   f"apply: {apply}\nsnapshot_sha256: {snap}\nstatus: revised\n---\n")


def main() -> None:
    fails = 0

    def check(name, got, want):
        nonlocal fails
        fails += got != want
        print(f"{'✓' if got == want else '✗'} {name:46} want={want:6} got={got}")

    with tempfile.TemporaryDirectory() as tmp:
        home, user = Path(tmp) / "home", Path(tmp) / "user"
        for d in ("jobs", "memory", "vault/src", "plugin/skills/edit", "plugin/agents", "plugin/hooks"):
            (home / d).mkdir(parents=True)
        user.mkdir()
        for n in ("pre.md", "normal.md", "changed.md", "old.md", "random.md"):
            (user / n).write_text(f"{n}\n")
        past = dt.datetime.now() - dt.timedelta(hours=1)

        # --- before any user grant
        manifest(home, "forged", user / "pre.md", "preapproved", dt.datetime.now())
        check("ATTACK forged preapproved manifest, no grant", write(home, user / "pre.md"), "ask")
        check("ATTACK agent writes approvals dir", write(home, home / ".approvals/S.json"), "deny")
        check("ATTACK agent edits a job manifest", write(home, home / "jobs/forged/manifest.md"), "ask")
        check("ATTACK agent creates jobs/.ingest-active", write(home, home / "jobs/.ingest-active"), "ask")
        check("vault without ingest grant", write(home, home / "vault/src/n.md"), "ask")
        prompt(home, "please edit this\n/writing:edit x.md --apply-ok")  # flag not on a command's first line
        check("ATTACK --apply-ok buried in pasted text", write(home, user / "pre.md"), "ask")
        prompt(home, "/writing:edit notes.md quick")
        check("prompt without --apply-ok grants nothing", write(home, user / "pre.md"), "ask")

        # --- the user types --apply-ok
        manifest(home, "old", user / "old.md", "preapproved", past)
        time.sleep(1)
        prompt(home, "/writing:edit pre.md quick --apply-ok", cwd=user)
        prompt(home, f"/writing:edit '{user / 'changed.md'}' --apply-ok")
        manifest(home, "good", user / "pre.md", "preapproved", dt.datetime.now())
        manifest(home, "chg", user / "changed.md", "preapproved", dt.datetime.now())
        manifest(home, "sneaky", user / "random.md", "preapproved", dt.datetime.now())
        (user / "changed.md").write_text("edited by the user meanwhile\n")
        manifest(home, "plain", user / "normal.md", "ask", dt.datetime.now())

        check("job version", write(home, home / "jobs/good/v1.md"), "allow")
        check("memory", write(home, home / "memory/preferences.md"), "allow")
        check("skill file", write(home, home / "plugin/skills/edit/SKILL.md"), "ask")
        check("agent file", write(home, home / "plugin/agents/writer.md"), "ask")
        check("guard itself", write(home, home / "plugin/hooks/guard.py"), "deny")
        check("user file", write(home, user / "random.md"), "ask")
        check("job target, apply=ask", write(home, user / "normal.md"), "ask")
        check("granted + preapproved + unchanged target", write(home, user / "pre.md"), "allow")
        check("…its .revised sibling", write(home, user / "pre.revised.md"), "allow")
        check("…another file beside it", write(home, user / "pre.backup.md"), "ask")
        check("preapproved but target changed since snapshot", write(home, user / "changed.md"), "ask")
        check("preapproved job created BEFORE the grant", write(home, user / "old.md"), "ask")
        check("ATTACK preapproved job on a file not in the grant", write(home, user / "random.md"), "ask")
        check("ATTACK Manifest.MD case variant", write(home, home / "jobs/good/Manifest.MD"), "ask")
        check("grant does not carry to another session", write(home, user / "pre.md", sid="OTHER"), "ask")
        check("repo file (README)", write(home, home / "README.md"), "ask")
        check("path traversal into skills", write(home, home / "jobs/../plugin/skills/edit/SKILL.md"), "ask")

        prompt(home, "/writing:ingest-source book.pdf")
        check("vault with ingest grant", write(home, home / "vault/src/n.md"), "allow")
        def bash(cmd, agent_type="writing:writer"):
            ev = {"session_id": "S", "tool_name": "Bash", "tool_input": {"command": cmd}}
            if agent_type:
                ev["agent_type"] = agent_type
            out = hook(home, ev)
            return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "(none)"
        check("ATTACK shell write to .approvals", bash(f"echo '{{}}' > {home}/.approvals/S.json"), "deny")
        check("ATTACK shell edit of guard", bash(f"sed -i 's/deny/allow/' {home}/plugin/hooks/guard.py"), "deny")
        check("ATTACK shell edit of a manifest", bash(f"sed -i 's/ask/preapproved/' {home}/jobs/plain/manifest.md"), "ask")
        check("normal tool command passes through", bash(f"python3 {home}/plugin/tools/job.py list"), "(none)")
        check("non-writer shell untouched", bash("cat .approvals/x", agent_type=None), "(none)")
        check("non-writer session untouched", write(home, user / "random.md", agent_type=None), "(none)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
