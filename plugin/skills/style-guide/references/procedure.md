# Revision procedure

## Order: top-down, beginnings first
Fix what readers meet first and what frames everything else. A perfect sentence inside a misframed paragraph is wasted effort ([[Spend revision effort on beginnings]]).

1. **Intent.** Write a three-line intent statement: *purpose* (what the reader should know, think or do), *reader* (who they are and what they already know), *main point* (one or two sentences). If you can't state the main point, that is the first problem. Ask about it, or log it in trust mode.
2. **Document** (`lens-global`):
   - Does the introduction motivate (shared context, then problem as condition + cost, then the point or solution)?
   - Is the main point stated where readers expect it?
   - Do the parts follow a visible order?
   - Does the conclusion restate the point and its significance?
3. **Sections and paragraphs** (`lens-global`):
   - Does each unit open with a short issue that ends in its point, with key terms named?
   - Is every sentence relevant to the point?
4. **Flow** (`lens-cohesion-emphasis`):
   - Do topic strings stay consistent, with old information before new?
   - Is the stress position used, and are themes threaded through?
5. **Sentence clarity** (`lens-actions-characters`): characters as subjects, actions as verbs. Unpack nominalizations, choose passive deliberately.
6. **Sentence shape and concision** (`lens-concision-shape`): quick openings, short subjects, no sprawl, no redundancy or empty metadiscourse, calibrated hedges.
7. **Grace** (`lens-elegance`): only at key moments (opening, section ends, conclusion), and only in thorough mode or on request.
8. **Correctness pass** (`correctness-folklore`, `punctuation-sources`): fix only real errors, never folklore. Leave citations and quotations exactly as they are.

## Quick mode triage (one pass, no subagents)
1. Run `textstats.py` on the text.
2. Global light: can you find the main point in the first paragraph (or the first section of a long text)? If not, note it as an assumed question. Don't restructure in quick mode unless the text is short (under ~300 words) and the fix is obvious.
3. For every sentence flagged NOM, PASS, EXPL, INTRO, LONG or META, apply the matching checks: `lens-actions-characters` AC1–AC4 and `lens-concision-shape` (the checks it marks for quick mode).
4. **Flow, for every paragraph of two or more sentences, flagged or not** (`lens-cohesion-emphasis`):
   - Read the topic string (the textstats `topic_string`: each sentence's first ~7 words). Do the subjects name the same few characters or concepts? If they wander, choose the paragraph's topic and make it the subject of most sentences.
   - Old before new: does each sentence open with something the reader has already met, and end with what is new or complex? Reorder (or use the passive) where it doesn't.
   - Stress: does each sentence end on its most important words? Move trailing qualifications, hedges and attributions to the left.
   - Sentences that repeat the same topic back to back can often be **combined** into one, with a shared subject or coordinated verbs.
   - Vague back-references (`lens-cohesion-emphasis` CE12): a sentence that opens with a bare *this, that, it, these, because of this, for this reason* makes the reader reconstruct the link. Name what it points to: "This delay…", "Because the fleet was overextended…".
5. **Point first, for every sentence of about 25+ words or one that opens with an introductory phrase or clause, flagged or not** (`lens-concision-shape` CS1, CS2): find the sentence's claim. If it sits in the middle or at the end, open with it in a short main clause, and attach the explanation or support after it. The exception is a deliberately suspended sentence at a key moment ([[Suspend the climax with parallel openers]]).
6. Unflagged sentences: one read for redundancy and obvious implications.
7. Keep the paragraph structure unless a paragraph has no point at all.

## Thorough mode
1. Run textstats, then dispatch four `writing:diagnostician` agents in parallel (lenses: global, cohesion-emphasis, actions-characters, concision-shape). Pass each one the text path, the textstats, the intent and the relevant preferences.
2. Synthesize the findings into a **revision plan** in `decisions.md`. Order it top-down. Merge findings that overlap, and resolve conflicts between lenses (below).
3. Extract **decisions** (structure, point, cuts, framing): ask the user, or with trust on, assume and log.
4. Revise top-down into `v1`. For contested key passages (the introduction, a thesis sentence, a conclusion), write 2–3 alternatives in `variants/` and let the user choose (or choose yourself and log it).
5. Run the meaning checker, then the review, then `v2`.

## When lenses conflict
- **Cohesion beats single-sentence clarity.** A passive that keeps old information first is better than an active that breaks the flow ([[Favor cohesion over single-sentence clarity]]).
- **Character subjects vs. topic strings:** pick the character the *passage* is about, and keep that character as the subject.
- **Concision vs. signposting:** in documents over ~3 pages, keep the metadiscourse that maps the structure, and cut the rest.
- **Concision vs. hedging:** hedges that express real uncertainty are content. Remove only stacked or reflexive hedges, and leave research claims alone unless the user says otherwise.
- **Elegance vs. clarity:** clarity first. Ornament never at the cost of a clear subject and verb.

## Proportion
Leave sentences that pass every check alone. **A sentence that fails a check gets rewritten fully, not patched.** Swapping one noun for a gerund, or moving one phrase while the abstract subject stays, is the most common under-edit. Rebuild the sentence around its character and action, then restore the author's terms and voice. Combining or splitting sentences is fine when the flow checks call for it. A good edit reads in the author's voice, but it doesn't have to be small. Track every non-trivial change's reason in `decisions.md` (lens + check id), so the user can ask "why?".
