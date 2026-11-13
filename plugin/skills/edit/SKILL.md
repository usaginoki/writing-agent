---
name: edit
description: Edit, rewrite or revise existing text (a file or pasted text) for clarity, concision and structure. Work happens in a job workspace and the original is untouched until applied. Supports quick or thorough mode and trust or ask.
argument-hint: "<file | paste> [quick|thorough] [--trust|--ask] [--apply-ok] [--genre paper|essay|notes|memo]"
---

# Edit / rewrite

Arguments: `$ARGUMENTS`. `HOME` = `${user_config.home_dir}`. Load the `style-guide` skill if it isn't already in context, and read `references/procedure.md`.

## 0. Parse
- **Target:** a file path, or pasted text (in the arguments or earlier in the conversation).
- **Mode:** `quick` or `thorough`. If unstated, follow the writer's defaults (thorough for papers, essays and anything over ~800 words; quick for notes and short texts).
- **Trust:** `--trust` / `--ask`. Defaults: on in quick mode, off in thorough mode.
- `--apply-ok` → the job is created with `--apply preapproved`.
- **Genre:** infer it from the form and extension (`.tex` → paper) unless given.
- If the user asks only for a review or critique ("what's wrong with this?"), stop after step 3 and report the findings. Don't revise.

## 1. Intake
1. Create the job:
   `python3 HOME/plugin/tools/job.py new <path|-> --mode <m> --trust|--no-trust --apply <ask|preapproved> --genre <g>`
   For pasted text, pipe it in with `-`. Note the printed job directory (`JOB`).
2. Read the memory files: `memory/preferences.md`, plus `memory/genres/<genre>.md` if it exists.
3. Write the **intent statement** (purpose · reader · main point) into the `# Intent` section of `JOB/manifest.md`. Infer it from the text.
   - Thorough with trust off: confirm it with the user in one AskUserQuestion. Offer your inferred version, an alternative reading if the text is ambiguous, and "let me state it".
   - Otherwise: log it as an `assumed` question (Q1) in `questions.md`.
4. For docx, tell the user once that complex formatting may not survive and that the result will be a `.revised.docx` beside the original.

## 2. Diagnose
- Run `python3 HOME/plugin/tools/textstats.py JOB/v0.<ext> --json > JOB/textstats.json`, then the brief form for your own reading.
- **quick:** diagnose it yourself, following the "Quick mode triage" in `procedure.md`.
- **thorough:** dispatch **four `writing:diagnostician` agents in parallel**, one message with four Agent calls, for the lenses `global`, `cohesion-emphasis`, `actions-characters` and `concision-shape`. Give each one: the lens, the text path, the textstats path, the intent, the genre, the relevant preferences, and `home: HOME`. Add `elegance` only if the user asked for polish.

## 3. Plan and decide
1. Merge the findings into a top-down revision plan in `JOB/decisions.md`: findings by level, conflicts resolved (see `procedure.md`), each planned change tagged with lens and check id.
2. Collect the **decisions** (each diagnostician's `DECISIONS`, plus your own): main point, framing, structure and order, cuts, focus, terminology, register.
3. Number each decision as a question in `JOB/questions.md`:
   ```
   ## Q2 · open · structure
   The argument appears in ¶5, but the introduction promises a survey. Which should the introduction promise?
   - options: a) the argument (recommended): move the claim into the intro · b) keep the survey framing, sharpen it · c) other
   **Assumed:**
   **Answer:**
   ```
4. **Trust off:** ask now. Use AskUserQuestion (up to 4 per call, recommended option first), or the UI `questions` section if it's warranted (see the `writing:ui` skill). Record the answers in `questions.md` (status `answered`).
   **Trust on:** fill in `**Assumed:**` with your choice and a one-line reason, set the status to `assumed`, and continue.

## 4. Revise
- Write `JOB/v1.<ext>` (same format as `v0`), top-down, following the plan. Preserve all protected constructs (see `references/latex.md`) and run the count check for LaTeX/Markdown.
- Thorough mode: for 1–3 key passages where reasonable versions differ (the thesis sentence, the opening, the conclusion), write `JOB/variants/<name>.md` with 2–3 options, and let the user choose (trust off) or choose and log (trust on).
- `python3 HOME/plugin/tools/job.py set JOB current=v1 status=revised`

## 5. Meaning check
- Run the `writing:meaning-checker` agent with the original (`v0`), the revision (`v1`), the hunks (`job.py hunks JOB v0 v1`), the intent, the meaning-related preferences, and `home: HOME`. Always do this in thorough mode. In quick mode, do it when you restructured or cut more than a sentence of substance.
- `block` findings: fix them in `v1` directly.
- `ask` findings:
  - Trust off: show the original and revised span, and ask "Does this preserve what you meant?" (options: keep the revision / revert / adjust: tell me). In the UI, use a `meaning` section.
  - Trust on: revert to the original wording, and log it as an `assumed` question that offers the revision.
- `note` findings: keep them for the summary.

## 6. Review (thorough, trust off)
- `python3 HOME/plugin/tools/job.py hunks JOB v0 v1` gives the paragraph-level hunks.
- **Few hunks (≤ 5), or terminal-only:** show each one as before/after with a one-line reason, then ask accept / reject / edit for each (batch them with AskUserQuestion, multiSelect "which to reject").
- **Many hunks:** use the UI `hunks` section (see `writing:ui`).
- Apply the decisions into `JOB/v2.<ext>` and set `current=v2`. Any comment that expresses a durable preference goes to memory (write and announce).

## 7. Finish
Give the summary in the format described in the writer agent: changes by lens, the version path, assumed and open questions with how to answer them, meaning notes, memory updates, and the next step. For pasted text, also print the final text.

Don't apply automatically. Applying is `writing:apply`. The exception is `apply=preapproved`: then proceed straight to the apply procedure after the summary.
