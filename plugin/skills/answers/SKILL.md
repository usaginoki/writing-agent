---
name: answers
description: Process the user's answers to questions logged by the writing agent (trust mode), and make targeted adjustments to the job's current version. Also lists open questions for a job.
argument-hint: "[job] [answers in free text]"
---

# Answers → fast adjustments

Arguments: `$ARGUMENTS`. `HOME` = `${user_config.home_dir}`.

1. **Find the job.** Use the one named in the arguments, otherwise the most recent job with unresolved questions (`python3 HOME/plugin/tools/job.py list`).
2. **Collect the answers** from all channels:
   - `**Answer:**` fields the user filled in `JOB/questions.md`;
   - new files in `JOB/feedback/` (UI submissions);
   - answers in the arguments or the chat ("Q3: b", "keep the survey framing").
   If there are none and trust is off, present the unresolved questions: AskUserQuestion for up to 4, or the UI `questions` section if there are more. With trust on, just list them and stop.
3. **For each answer that differs from what was assumed:**
   - Find what that assumption affected, using `decisions.md`, which tags changes to their question ids.
   - Make the **minimal targeted change** in a new version: copy `current` to `v<n+1>` and edit only the affected passages. Don't re-run the whole pipeline. The exception is a structure question, which may require re-planning the affected sections.
   - Set the question's status to `answered` and record what changed.
   Answers that confirm the assumption: mark them `answered`, with no change.
4. **Meaning check:** run `writing:meaning-checker` if the adjustments went beyond a sentence.
5. **Memory:** an answer may reveal a durable preference ("always frame papers conceptually"). If so, write and announce it.
6. **Summary:** list each answered question with its result, give the new version path, and state any remaining open questions.
