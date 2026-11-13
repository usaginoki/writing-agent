---
name: apply
description: Apply a finished job version to the user's original file. It checks the original is unchanged, shows the diff, and writes only with approval (or pre-approval). docx is exported as a new .revised.docx and never overwritten.
argument-hint: "[job] [version]"
---

# Apply a version to the original

Arguments: `$ARGUMENTS`. `HOME` = `${user_config.home_dir}`. Default job: the most recent one. Default version: the manifest's `current`.

1. Run `python3 HOME/plugin/tools/job.py status JOB` to see the target, format, apply mode and versions.
   - A target of `(pasted)` means there is nothing to apply. Print the final text, or offer to save it where the user wants (which needs their approval of the path).
2. **Safety check:** run `python3 HOME/plugin/tools/job.py check JOB`.
   - If the result is `CHANGED`, **stop**. The user edited the original after the snapshot. Offer two options:
     - (a) re-run the edit on the new original;
     - (b) show a three-way view (snapshot vs current original vs revision), so the user can merge.
   - Never overwrite the original in this state.
   - If the result is `MISSING`, ask where to write.
3. **Show the change.** Run `job.py diff JOB v0 <version>` and summarize it: N paragraphs changed, the main moves. For long diffs, offer the UI `hunks` view. Otherwise show the most significant hunks in the terminal.
4. **Approval:**
   - `apply: preapproved`: proceed, and say "applying (pre-approved)".
   - Otherwise, ask once: "Apply <version> to <target>?" with the options: apply / apply to a copy (`<name>.revised.<ext>`) / not now.
5. **Write**, using the **Write tool only** (never Bash). The guard hook will also show its own confirmation unless the job is pre-approved.
   - md/txt/tex: Write the version's full content to the target path.
   - docx: `uv run -q --project HOME python HOME/plugin/tools/convert.py to-docx JOB/<version>.md "<dir>/<stem>.revised.docx" --ref "<target>"`. Pre-approval, or the user's answer in step 4, covers this new file. Never overwrite the original `.docx`.
6. Run `job.py set JOB status=applied applied_version=<version>` and report the path written.
