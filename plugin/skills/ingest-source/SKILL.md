---
name: ingest-source
description: Add a new knowledge source (a book, guide or article as PDF, docx, md or epub) to the writing vault. Sonnet subagents extract principles, diagnostics and patterns into Obsidian notes, then the skill PROPOSES updates to the style guide, which need explicit approval.
argument-hint: "<path to source> [slug]"
disable-model-invocation: true
---

# Ingest a new source

Arguments: `$ARGUMENTS`. `HOME` = `${user_config.home_dir}`. Conventions: `HOME/vault/_conventions.md`. Reference run: `HOME/vault/style-williams-bizup/` (see its `_source/sections.json` and `00 Index.md`).

## 1. Prepare
1. Choose a slug: `<short-title>-<author(s)>`, lowercase with hyphens. Confirm it with the user.
2. Run `touch HOME/jobs/.ingest-active`, which lets the guard allow vault writes during the ingest. Remove the file at the end, **even on failure**.
3. Create `HOME/vault/<slug>/_source/` and **move** the source file into it (ask first if the file lives outside HOME).

## 2. Extract
- **PDF:** read the table of contents (Read with `pages`, first ~10 pages). Find the PDF page offset by checking that a chapter's first page matches with `pdftotext -f N -l N`. Write `_source/sections.json` (id, title, start, end, book pages), then run:
  `uv run -q --project HOME python HOME/plugin/tools/extract_source.py <pdf> _source/sections.json _source/text`
- **docx, epub, html:** run `convert.py to-md`, then split on top-level headings into `_source/text/<id> <title>.md`.
- **md:** split on headings.
- Check one section file for extraction quality (italics kept, no garbage).

## 3. Canonical concepts
- Build a list of the source's key terms from its glossary or index (or skim it). Compare the list against the existing concepts in other sources' `concepts/` folders.
  - A concept that already exists elsewhere under the same name: use the note name `<Concept> (<slug>)` to avoid wikilink collisions. Link to the existing concept in "Related".
  - Assign each concept note to exactly **one** worker.

## 4. Parallel extraction (Sonnet)
Split the sections into batches of about 8–12k words, using at most 8 batches. Dispatch one `general-purpose` agent per batch with `model: sonnet`, all in a single message. Each brief must include:
- the vault root and an instruction to follow `_conventions.md`;
- the input file paths and the markup legend;
- the output folders under `vault/<slug>/`;
- the concept notes that worker owns, and the canonical names it may link to;
- "link only principles you create";
- a final reply that lists the notes created.

This is the same brief used for the Williams vault. The scope paragraph changes per batch.

## 5. Synthesize (you)
- Fix note-name collisions, since two workers may produce the same diagnostic. Merge them; don't overwrite.
- Run the link check for dangling `[[links]]`. Make sure every principle has an example and a "When not to apply" section.
- Add cross-lesson "Across lessons:" links between related principles.
- Write `vault/<slug>/00 Index.md`, organized by revision level (document → section → paragraph → sentence → grace), like the reference index.
- **Cross-source links:** where a principle agrees with or contradicts a principle in another source, add `- Other sources: [[…]] (agrees|differs: …)`.

## 6. Propose style-guide updates (needs permission)
- Compare the new source with `HOME/plugin/skills/style-guide/references/*.md`. Look for new checks, better examples, exceptions, and **conflicts** between sources.
- Write the proposal to `HOME/jobs/ingest-<slug>-proposal.md`:
  - per reference file, the additions and changes as a diff or exact text;
  - conflicts, each with both positions and a recommendation;
  - new reference files if the source covers new ground (e.g. a `lens-scientific-figures.md`).
- Present a summary and ask: apply all / apply selected / don't apply. **Edit the skill files only after an explicit yes.** The guard hook will confirm each write as well.
- Add the source to the list of current sources in the `style-guide` SKILL.md. That is a skill edit too, so it falls under the same approval.

## 7. Finish
Run `rm HOME/jobs/.ingest-active`. Report the number of notes by type, the link-check result, and the proposal status.
