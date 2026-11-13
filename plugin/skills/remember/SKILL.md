---
name: remember
description: Record a writing preference or piece of feedback in the writing agent's memory (separate from skills), or show and edit what is remembered.
argument-hint: "<preference> | show | forget <item>"
---

# Remember a preference

Arguments: `$ARGUMENTS`. `HOME` = `${user_config.home_dir}`. Memory lives in `HOME/memory/`:
- `preferences.md`: durable, general preferences, in sections (Voice & register, Never change, Structure, Sentences & words, Formatting, Workflow & UI);
- `genres/<genre>.md`: preferences for one genre (paper, essay, notes, memo);
- `feedback-log.md`: a dated, append-only log of raw feedback.

## Record (default)
1. Turn the feedback into a **specific, actionable** preference with its scope: "Keep my hedges in research papers", not "be careful". Where the preference isn't obvious, record why.
2. Decide where it goes: general → `preferences.md` (pick the section); genre-specific → `genres/<genre>.md` (create the file from the section headings in `preferences.md` if needed).
3. **Check for conflicts** with existing entries. If one exists, update that entry instead of adding a contradicting one. If unsure, ask.
4. Write it, append to `feedback-log.md` (`- YYYY-MM-DD · <raw feedback> → <where recorded>`), and announce: `📝 Remembered: … (memory/…)`.
5. If the preference contradicts the style guide, still record it (memory wins). Mention which style-guide check it overrides, so diagnosticians honor it. **Do not edit skills.** If the user wants the style guide itself changed, propose the diff and wait for an explicit "yes".

## show
Print `preferences.md`, the genre files, and the last 10 log lines.

## forget <item>
Remove or adjust the matching entry. Log the removal and announce it.
