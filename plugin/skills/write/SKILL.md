---
name: write
description: Draft new prose (essay, research paper section, note, memo) from notes, an outline, sources or a prompt. Steps are intent, then structure options (a decision), then the draft, then the edit pipeline. Output goes to a job workspace.
argument-hint: "<notes file | prompt> [quick|thorough] [--trust|--ask] [--genre ...] [--out <path>]"
---

# Write a new draft

Arguments: `$ARGUMENTS`. `HOME` = `${user_config.home_dir}`. Load the `style-guide` skill (`procedure.md`, `lens-global.md`, `genres.md`).

The principles are revision tools, not drafting rules ([[Draft first then revise with principles]]). So: get the structure right, draft fluently, then run the edit pipeline on the draft.

## 1. Intake
- Create a job from the source material: `job.py new <notes-file|-> --mode <m> ...`. For a bare prompt, pipe it in with `-`. The material becomes `v0` (the notes), not the draft.
- `--out <path>`: the eventual target for the draft. Pass it at creation: `job.py new <notes|-> --out <abs path> ...`. Apply creates the file, and won't overwrite an existing one without asking. The target can't be changed later.
- Read memory (preferences and genre).
- Establish the intent: purpose · reader · **main point**. If the material doesn't yield a main point, that's a decision. Ask (trust off), or propose the strongest candidate and log it (trust on).

## 2. Structure (a key decision)
- Write 2–3 **outline options** in `JOB/variants/outlines.md`. Each one has a title, a one-line rationale, and its sections, each with a one-line point. Base them on `lens-global.md`: the introduction pattern (practical vs conceptual problem), the point placement, and the order (chronological, coordinate or logical).
- **Trust off:** let the user choose. Use the UI `structure` section if the outlines are long or the user wants to reorder sections; otherwise use AskUserQuestion with the outline in each option's preview. **Trust on:** choose, and log it as `assumed` with the alternatives.

## 3. Draft
- Write `JOB/v1.md` (or `.tex` if the target is LaTeX) following the chosen outline:
  - Introduction: shared context → problem (condition + cost) → point, with the key terms named at the end of the point.
  - Each section and paragraph: a short issue that ends in its point, then the discussion, using the key terms consistently.
  - Sentences: characters as subjects, actions as verbs, old before new.
- Use only claims supported by the user's material. Mark gaps as `[TODO: evidence for …]` rather than inventing facts, citations or numbers. Log each gap as a question.
- Match the user's voice from memory and from any samples of their writing in the material.

## 4. Revise and check
Continue with `writing:edit` steps 2–7 on `v1`. The draft is the text being edited, and the meaning check compares the draft against the **notes and the intent**, so any claim not supported by the notes gets flagged.
