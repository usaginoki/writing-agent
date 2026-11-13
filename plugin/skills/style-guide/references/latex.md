# Editing source formats safely

## LaTeX
**Never change**, byte for byte:
- the preamble, `\begin{…}`/`\end{…}` and environment names, `\label{}`, `\ref{}`, `\eqref{}`, `\cite*{}`, `\autoref{}`, `\url{}`, `\href{}{}` targets;
- math: `$…$`, `\(…\)`, `\[…\]`, and `equation`, `align`, etc.;
- `verbatim`, `lstlisting`, `minted`, `tikzpicture`, `tabular` column specs, figure and table bodies except caption prose;
- `%` comments (unless asked), macros the user defined, and non-breaking spaces `~` before `\cite`/`\ref`;
- `\` line breaks and spacing commands in title blocks.

**Prose you may edit:** paragraph text, the text arguments of `\section{}`, `\caption{}` and `\footnote{}`, and the arguments of `\emph{}` and `\textbf{}`. Keep each command's wrapping around the same semantic words.

**Practice:**
- Edit paragraph by paragraph. Keep the source line structure where possible (many authors use one sentence per line, so preserve that habit).
- When moving a sentence that contains a `\cite`, move the citation with its claim.
- Keep quotation marks in LaTeX style (` ``…'' `) if the source uses them.
- After revising, check that the counts of `\cite`, `\ref`, `\label`, `$` and `\begin` are identical between the original and the revision (`grep -o` counts). Any difference is a bug to fix before showing the result.

## Markdown / Obsidian
- Preserve YAML frontmatter, `[[wikilinks]]` (including `|alias` and `#heading`), `![[embeds]]`, `#tags`, `^block-ids`, callouts (`> [!note]`), code blocks and inline code, link URLs, footnote markers, and HTML.
- Headings can be reworded only if nothing links to them. If unsure, keep them.
- Keep list nesting and the list markers' style.
- Run the same count check for `[[`, `](`, `` ``` `` and `^`.

## docx
- The job works on `v0.md` (converted with pandoc). Formatting beyond headings, lists, emphasis, tables and footnotes may be lost. Tell the user this at intake.
- Deliver with `convert.py to-docx vN.md <dir>/<name>.revised.docx --ref <original.docx>`. Never overwrite the original `.docx`.

## Pasted text
- No target file. Deliver the final version in chat (and in the job directory). Apply is not needed.
