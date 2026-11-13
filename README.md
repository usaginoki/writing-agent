# Writing agent

A Claude Code plugin for writing, rewriting and editing essays, notes and research papers. Its goal is clear, concise, well-structured prose. It is grounded in a knowledge vault distilled from writing books (currently Williams & Bizup, *Style: Lessons in Clarity and Grace*).

## Use
```bash
claude --agent writing:writer          # dedicated writer session, from any directory
alias write='claude --agent writing:writer'
```
Inside any session, the skills are also available as commands:

| command | does |
|---|---|
| `/writing:edit <file\|paste> [quick\|thorough] [--trust\|--ask] [--apply-ok]` | revise existing text in a job workspace |
| `/writing:write <notes\|prompt> …` | outline options, then a draft, then the edit pipeline |
| `/writing:answers [job]` | apply your answers to logged questions (trust mode) |
| `/writing:apply [job] [version]` | write an approved version to the original file |
| `/writing:remember <pref> \| show \| forget` | manage your preferences |
| `/writing:ingest-source <file>` | add a new book or guide to the vault |

**Modes:**
- **quick**: one pass. Trust mode is on: no interruptions, and decisions are logged to `questions.md`.
- **thorough**: four parallel diagnosticians, decisions asked along the way, a meaning check, then a per-change review.

`--trust` / `--ask` override the default for either mode.

## Safety model
- **Your files are never edited in place.** Each task gets `jobs/<date>-<slug>/`, holding `original.*`, `v0…vN`, `variants/`, `questions.md`, `decisions.md`, `diffs/` and `feedback/`. `/writing:apply` checks that the original hasn't changed since the snapshot, shows the diff, and writes only with your approval, or with `--apply-ok` given in advance.
- **docx** files are never overwritten. You get `<name>.revised.docx` next to the original.
- **Guard hook** (`plugin/hooks/guard.py`): in writer sessions, writes to `jobs/` and `memory/` go through freely. Writes to your files, the skills, the agents and job manifests trigger a permission prompt, and the hook can never edit itself.
- **Approvals come only from you.** A `UserPromptSubmit` hook records a grant when *you* type `--apply-ok` on a `/writing:edit` or `/writing:write` command line, or run `/writing:ingest-source`. The grant names the specific file, lasts for that session (up to 12 h), and lives in `.approvals/`, which the agent may not write to. A pre-approved write also requires the file to be unchanged since the job's snapshot. So neither the agent nor a prompt injection inside a document it edits can approve its own writes. Run `python3 plugin/hooks/test_guard.py` to check every case, attacks included.

## Layout
```
plugin/                 the plugin (loads in place from here)
  agents/               writer (main), diagnostician (sonnet), meaning-checker (sonnet)
  skills/               edit, write, answers, apply, remember, ingest-source, ui, style-guide (+ references/)
  hooks/guard.py        write guard
  tools/                job.py, textstats.py, convert.py, extract_source.py
  ui/                   server.py + templates/review.html (optional browser UI)
vault/                  Obsidian vault: one folder per source, plus _conventions.md
memory/                 your preferences (agent-editable, separate from skills)
jobs/                   per-task workspaces (git-ignored)
evals/                  test cases from the book's exercises + judge rubric
```

## Memory vs skills
- `memory/` holds **your** preferences. The writer records feedback there right away and tells you in one line: `📝 Remembered: …`. Edit the files any time. Memory overrides the style guide.
- `plugin/skills/` holds **craft knowledge**. The writer may only *propose* changes to it, and the guard hook asks before any write.

## UI
Set `ui: auto | on | off` in `memory/preferences.md`. The UI is a single ephemeral local page (stdlib Python, no dependencies) that combines question forms, word-level diff review with accept/reject/edit, outline choice with reordering, meaning checks, and variant picking. It closes after one submission. Everything also works in the terminal.

## Sources are not included
The vault's notes are compressed paraphrase with short illustrative examples. The source books themselves (`vault/<source>/_source/*.pdf`, the extracted full text in `_source/text/`) and the eval cases built from the book's exercises (`evals/cases/`) are copyrighted, so they are git-ignored and stay local. To rebuild them, put your own copy of the book in `_source/` and run `extract_source.py` with the committed `sections.json`. To add a new source, use `/writing:ingest-source`.

## Setup (already done on this machine)
```bash
uv sync                                                       # pymupdf4llm, pypandoc-binary
claude plugin marketplace add ~/Workspace/My/agents/writing
claude plugin install writing@writing-local --config home_dir=$HOME/Workspace/My/agents/writing
```
