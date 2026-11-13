---
name: ui
description: How the writing agent collects decisions and feedback, either in an optional ephemeral browser page (questions, diff hunks, structure options, meaning checks, variants) or in the terminal. Covers when to use each, the page JSON schema, and how to launch and read results.
user-invocable: false
---

# Interaction: browser UI or terminal

`HOME` = `${user_config.home_dir}`. The setting is `ui:` in `HOME/memory/preferences.md`: `auto` (default), `on` or `off`.

## When to use the browser (`auto`)
| situation | auto choice |
|---|---|
| 1–4 short questions | terminal (AskUserQuestion) |
| 5+ questions, or questions with long context | UI `questions` |
| review of ≤ 5 hunks | terminal |
| review of > 5 hunks | UI `hunks` |
| choosing between outlines, or reordering sections | UI `structure` |
| 2–3 alternative passages to compare | UI `variants` (terminal if they're short) |
| meaning-check flags | terminal if ≤ 3, otherwise UI `meaning` |

One page can combine several sections (e.g. `meaning` + `questions`). Prefer one page per decision point over many small pages. With `on`, use the UI for every multi-item interaction; with `off`, never use it.

## Launch
1. Write the page JSON to `JOB/feedback/page-<name>.json` (schema below).
2. Run in the **background**: `python3 HOME/plugin/ui/server.py --job JOB --data JOB/feedback/page-<name>.json`
   - It prints `UI http://127.0.0.1:<port>/`. Tell the user the URL in one line (the browser opens automatically), and mention that answering in the terminal still works.
   - When the user submits, the process prints `FEEDBACK <path>` and exits, and you get notified. Read that JSON. On `TIMEOUT` (default 1 h), fall back to the terminal.
3. While you wait, if the user answers in chat instead, accept that answer, and stop the server (TaskStop). The same holds the other way: the first answer wins.
4. Write the results into `questions.md` and `decisions.md` exactly as you would for terminal answers. The files are the record, and the UI is only a channel.
5. In the submission, `comment` together with `remember: true` means: write it to memory and announce it.

## Page schema
```json
{
  "name": "review-v1",
  "title": "Review: <document title>",
  "intro": "One or two sentences on what to do on this page.",
  "sections": [
    {"type": "questions", "title": "Decisions", "items": [
      {"id": "Q2", "topic": "structure", "text": "Which should the introduction promise?",
       "context": "optional longer explanation or quoted passage",
       "options": [{"key": "a", "label": "The argument", "detail": "move the claim from ¶5 into the intro"},
                   {"key": "b", "label": "The survey", "detail": "keep the framing, sharpen it"}],
       "recommended": "a", "multi": false, "allow_text": true}]},

    {"type": "hunks", "title": "Proposed changes", "items": [
      {"id": "h1", "before": "original paragraph", "after": "revised paragraph",
       "reason": "AC2: nominalizations → verbs; CE1: old info first"}]},

    {"type": "structure", "title": "Outline", "allow_reorder": true, "options": [
      {"key": "A", "title": "Problem-first", "rationale": "…",
       "sections": [{"title": "Introduction", "point": "…"}, {"title": "…", "point": "…"}]}]},

    {"type": "meaning", "title": "Did I keep your meaning?", "intent": "purpose · reader · point", "items": [
      {"id": "m1", "original": "…", "revised": "…", "concern": "hedge removed: 'may' → 'does'"}]},

    {"type": "variants", "title": "Opening paragraph", "groups": [
      {"id": "opening", "context": "why this passage matters", "options": [
        {"key": "1", "text": "…", "note": "conceptual framing"}, {"key": "2", "text": "…", "note": "…"}]}]}
  ]
}
```

## Submission (`feedback/<ts>-<name>.json`)
```json
{"page": "review-v1", "submitted": "…", "comment": "free text", "remember": false,
 "sections": [
   {"type": "questions", "answers": {"Q2": {"choice": "a", "text": ""}}},
   {"type": "hunks", "decisions": {"h1": {"action": "accept|reject|edit", "text": "edited text if edit", "comment": ""}}},
   {"type": "structure", "choice": "A", "order": ["Introduction", "…"], "comment": ""},
   {"type": "meaning", "verdicts": {"m1": {"verdict": "keep|revert|adjust", "text": "adjusted wording if adjust"}}},
   {"type": "variants", "choices": {"opening": {"choice": "2", "comment": "merge the first sentence of 1"}}}
 ]}
```
Unanswered items are omitted. Treat an omitted item as "accept the recommendation", or as "accept" for hunks, and say so in the summary.

## Terminal equivalents (always available)
- **questions:** AskUserQuestion, up to 4 per call. Use `options[].label`/`detail` and put the recommended option first with "(Recommended)". Free text goes through "Other".
- **hunks:** print each hunk as `h1 · reason`, then `- before` / `+ after` (trimmed to the changed sentences), and ask "Which hunks should I reject or edit?" (multiSelect over the hunks, plus "accept all").
- **structure:** AskUserQuestion with each outline in the option's `preview` (a markdown list of sections and their points). To reorder, the user writes the new order via "Other".
- **meaning:** for each flag, show the original and revised text, then ask "Does this preserve what you meant?" with the options keep revision / revert / adjust.
- **variants:** AskUserQuestion with each variant's text in `preview`.
