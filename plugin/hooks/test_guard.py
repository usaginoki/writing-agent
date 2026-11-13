"""Branch tests for guard.py. Run: python3 plugin/hooks/test_guard.py

Encodes the policy agreed in the plan. If you deliberately choose differently in decide()
(e.g. deny instead of ask for hooks/), update EXPECT to match: the tests document the policy.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).with_name("guard.py")


def run(home: Path, path: str, agent_type: str | None = "writing:writer") -> str:
    event = {"session_id": "t", "tool_name": "Write", "cwd": str(home), "tool_input": {"file_path": path}}
    if agent_type:
        event["agent_type"] = agent_type
    out = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(event), text=True, capture_output=True,
                         env={"WRITING_HOME": str(home), "PATH": "/usr/bin:/bin"}).stdout.strip()
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "(none)"


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "home"
        user = Path(tmp) / "user"
        for d in ("jobs/2026-01-01-a", "jobs/2026-01-01-b", "memory", "vault/src", "plugin/skills/edit",
                  "plugin/agents", "plugin/hooks"):
            (home / d).mkdir(parents=True)
        user.mkdir()
        target_ok, target_ask = user / "pre.md", user / "normal.md"
        (home / "jobs/2026-01-01-a/manifest.md").write_text(
            f"---\ntarget: {target_ok}\napply: preapproved\nstatus: revised\n---\n")
        (home / "jobs/2026-01-01-b/manifest.md").write_text(
            f"---\ntarget: {target_ask}\napply: ask\nstatus: revised\n---\n")

        EXPECT = [
            ("job version", home / "jobs/2026-01-01-a/v1.md", "allow"),
            ("memory", home / "memory/preferences.md", "allow"),
            ("skill file", home / "plugin/skills/edit/SKILL.md", "ask"),
            ("agent file", home / "plugin/agents/writer.md", "ask"),
            ("guard itself", home / "plugin/hooks/guard.py", "deny"),
            ("vault (no ingest)", home / "vault/src/note.md", "ask"),
            ("user file", user / "random.md", "ask"),
            ("job target, apply=ask", target_ask, "ask"),
            ("job target, preapproved", target_ok, "allow"),
            ("preapproved .revised sibling", user / "pre.revised.md", "allow"),
            ("other file beside preapproved", user / "pre.backup.md", "ask"),
            ("repo file (README)", home / "README.md", "ask"),
            ("path traversal into skills", home / "jobs/../plugin/skills/edit/SKILL.md", "ask"),
        ]
        fails = 0
        for name, path, want in EXPECT:
            got = run(home, str(path))
            ok = got == want
            fails += not ok
            print(f"{'✓' if ok else '✗'} {name:28} want={want:6} got={got}")

        (home / "jobs/.ingest-active").touch()
        got = run(home, str(home / "vault/src/note.md"))
        fails += got != "allow"
        print(f"{'✓' if got == 'allow' else '✗'} {'vault (ingest active)':28} want=allow  got={got}")

        got = run(home, str(user / "random.md"), agent_type=None)
        fails += got != "(none)"
        print(f"{'✓' if got == '(none)' else '✗'} {'non-writer session':28} want=(none) got={got}")
        sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
