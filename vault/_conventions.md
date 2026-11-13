---
type: meta
---
# Vault note conventions

The vault holds compressed, operational knowledge for the writing agent. Each source lives in `vault/<source-slug>/`. Notes are Obsidian markdown: YAML frontmatter, `[[wikilinks]]` by note name (no path, no `.md`), and tags.

## Folders per source
| folder | holds | naming |
|---|---|---|
| `_source/` | original file, `text/` extracted sections, `sections.json` | — |
| `lessons/` | one note per chapter/lesson | `L03 Actions` (same id as the extracted file) |
| `principles/` | one atomic, actionable principle per note | imperative phrase: `Make main characters subjects` |
| `concepts/` | a term the principles rely on | noun phrase, Title Case: `Nominalization`, `Topic String` |
| `diagnostics/` | a test procedure that finds a problem | `Diagnose …` / `… test`: `Topic string test` |
| `patterns/` | rewrite pattern tables (before → after shapes) | `Patterns - <subject>` |

## Frontmatter (all notes except _source)
```yaml
---
type: principle | concept | diagnostic | pattern | lesson
source: style-williams-bizup
lesson: L03            # lesson id(s); list if several
pages: 32-39           # BOOK page numbers (printed), not PDF
level: sentence | paragraph | section | document   # where it operates (principles/diagnostics)
lens: actions-characters | cohesion-emphasis | global-motivation | concision-shape | elegance | correctness | ethics | punctuation | sources
tags: [principle, clarity]
---
```

## Principle note body (the most important type)
```markdown
# <Imperative statement>

**Rule:** one or two sentences, operational.
**Why (reader effect):** what readers experience when it's broken / followed.

## Diagnose
- concrete, checkable steps (what to underline, count, look for)

## Revise
1. ordered steps

## Examples
> ✗ before (short, from the book)
> ✓ after (the book's revision)
(1–3 pairs; keep each sentence short; prefer the book's own examples)

## When not to apply / exceptions
- the book's caveats (genre, emphasis, deliberate effect, etc.)

## Related
- [[Concept]] · [[Other principle]] · [[L03 Actions]]
```

## Concept note body
Definition (compressed) · how to recognize it · why it matters for style · 1 example · Related links.

## Diagnostic note body
Purpose · step-by-step procedure · what result signals a problem · which principle(s) fix it.

## Lesson note body
One-paragraph summary of the argument · list of principles (links, with one-line gloss) · concepts introduced · diagnostics · the lesson's "Summing Up" condensed · notable quotes (≤2, short).

## Style of notes
- Compressed: bullets and short sentences; no filler; paraphrase rather than copy.
- Quote only examples and key formulations, briefly.
- Every principle MUST have ≥1 before/after example and a "when not to apply" section (write "None stated in source." if truly none).
- Cite book pages in frontmatter; inline `(p. 34)` for specific claims when useful.

## Graph colors (`.obsidian/graph.json`, matched by folder name, so new sources inherit them)
gold = `00 Index` · red = lessons · blue = principles · green = concepts · orange = diagnostics · purple = patterns. `_source/` is filtered out of the graph.
