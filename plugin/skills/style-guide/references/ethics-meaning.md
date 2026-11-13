# Ethics and meaning preservation (for the MEANING-CHECKER)

**Role:** compare ORIGINAL and REVISION. A revision may change how a text reads, never what it says, who did it, or how sure it is. Clarity edits that change meaning are failures, however well they read. The First Rule: write to others as you would have others write to you. [[Write to others as you would have them write to you]]

## What a revision must never do
1. Shift agency or responsibility (who did what, who decided, who is affected).
2. Strengthen a claim (remove hedges, add intensifiers/absolutes, convert possibility to fact).
3. Weaken a claim (add hedges, soften verbs, turn a finding into a suggestion).
4. Drop a qualification, condition, scope limit, exception, or caveat.
5. Oversimplify an idea that deserves its complexity; delete technical terms the expert reader needs.
6. Change causation, sequence, or logical relation (`because` / `although` / `therefore`).
7. Change the main point or its emphasis (what is old/background vs. new/important; what ends the sentence).
8. Add content the writer did not say (invented agents, numbers, examples, citations).
9. Drop content (data, names, dates, quantities, citations, quotations).
10. Alter quotations or citations in any way (see punctuation-sources).

## How to detect each (concrete comparisons)

### M1 Agency shift
- For each clause in the original, list subject + verb + object; do the same in the revision; align them by event.
- Flag: agent appears where the original had none (invented actor); agent vanishes (agentless passive, intransitive `occur`, nominalization); actor swapped (`we` -> `the system`); agent and affected party swapped by active/passive flip.
- Flag: a harmful or risky action moved from verb to nominalization, or from `you could be harmed` to `harm may occur`.
- Example: `The lab misreported the dose` -> `Dose errors occurred` = hides responsible party (block). `Mistakes were made` -> `We made mistakes` = adds responsibility the writer may not have intended (ask).
- OK: the original agent is unknown or irrelevant and the passive stays. [[Use the passive when the agent is unknown or irrelevant]]
- Links: [[Do not hide the responsible agent to deflect blame]] · [[Agency-hiding audit]] · [[Name the affected reader and the real actor in high-stakes text]] · [[Notice when grammar argues for you]]

### M2 Hedge and intensifier drift
- Extract every hedge (`may, might, suggest, appear, seem, tend, likely, some, many, most, usually, arguably`) and intensifier/absolute (`clearly, obviously, prove, show, all, every, always, never, completely`) from both texts.
- Compare per claim, not globally. Claim strength must be the same.
- Flag: hedge removed (`suggests` -> `shows`; `may reduce` -> `reduces`); hedge added; quantifier moved (`some` -> `many` -> `most` -> `all`); modal changed (`may` -> `will`, `could` -> `does`).
- Allowed: collapse stacked hedges to one (`seems to suggest that some... could` -> `suggests that`) when the strength stays the same; tell the user.
- Allowed: remove empty intensifiers (`very, obviously`) without changing strength.
- Example: `There seems to be some evidence that X might contribute` -> `Evidence suggests X contributes` = same-ish; `X causes` = strengthened (block).
- Links: [[Calibrate hedges]] · [[Calibrate intensifiers]] · [[Diagnose hedge and intensifier balance]] · [[Patterns - Hedges and intensifiers]] · [[Hedge]] · [[Intensifier]]

### M3 Dropped qualification
- List conditionals (`if, unless, only, provided`), scope limits (`in this sample, for adults, under 40C`), exceptions, `but` clauses, numbers with ranges/units.
- Each must have a counterpart in the revision. A concision cut that removes one is a block, not an "obvious implication" deletion.
- Check `delete obvious implications` edits: was it truly implied for the target reader? When unsure, ask.
- Links: [[Delete obvious implications]] · [[Be concise, not terse]] · [[Delete meaningless words]]

### M4 Oversimplification
- Compare content words: technical terms, definitions, steps, distinctions, nuance (`correlates` vs `causes`).
- Flag: a term replaced by a looser one; two distinct ideas merged; a nuance replaced by a slogan; a necessary nominalization expanded into a story with extra assumptions.
- Test: would the expert reader lose anything real? Would the ideas survive a one-line retelling?
- Keep technical terms and necessary structure; strip only avoidable complexity (unclear subjects, abstractions, long strings).
- Links: [[Be as complex as necessary and no more]] · [[Make ideas no simpler than they deserve and no harder than necessary]] · [[Keep useful nominalizations]]

### M5 Logic and sequence
- List connectors (`because, since, although, so, thus, but, if`) and their relations in both texts; compare.
- Flag: `although` -> `and` (concession lost), `since` temporal vs causal, `because` added with no basis, reordering of events that implied order.
- Links: [[Link revised clauses with precise connectors]] · [[Restore the real sequence of actions]] · [[Do not fake coherence with conjunctions]]

### M6 Emphasis and main point
- Compare the first and last 4 words of each sentence/paragraph; the point sentence; the key theme words.
- Flag: new information moved out of stress position; the main point demoted to a clause; a side point promoted; headline term removed; paragraph point no longer at the end of the opening segment.
- Reordering for old-before-new is legitimate only if the point is unchanged.
- Links: [[Stress]] · [[Old-New Information]] · [[Put the words you want emphasized in stress position]] · [[Point]]

### M7 Inflation and padding (the opposite failure)
- Revision must not add abstraction or words to sound deep. [[Do not inflate prose to seem deep]]

## Severity levels
| Level | Condition | Action |
|---|---|---|
| BLOCK | Strengthens/weakens a claim; drops a qualification, number, unit, or citation; invents or deletes an agent in a way that changes responsibility; alters a quote; reverses causation; invents content | Reject the edit; revert to the original wording |
| ASK USER | Ambiguity either way; collapsing hedges where strength may differ; passive -> active that requires guessing the actor; deleting an "obvious" implication; a simplification that loses nuance but gains access | Keep the original; present both versions; let the writer decide |
| NOTE | Emphasis shift of low consequence; hedge pile reduced with equal strength; intensifier removed; slight nuance loss on a minor point | Accept, record in the change log |
Escalate one level when the text is high-stakes: warnings, safety, medical, legal, financial notices, policy letters, research findings, anything a reader will act on or be harmed by. Name the affected reader and real actor. [[Reader-swap test]]

## Legitimate reasons to keep indirectness (do not "fix")
- The agent is unknown, irrelevant, or obvious (`records were kept`, `the president was reelected`).
- Kind softening the reader understands (`I'm afraid our funding didn't come through`). Test: does the reader reach the true meaning and keep the info needed to act? Motive is the test. [[Distinguish kind softening from deceptive indirectness]]
- The writer's real uncertainty: hedges are correct when evidence is incomplete. Confidence does not require flatness (Crick and Watson hedged).
- Abstract subjects in general principles or theory (`necessity constrains`) when the abstraction is the topic.
- Conventions of the field: passive in methods, `we` vs. impersonal; keep per the user's memory/preferences.
- Writer's deliberate stance: a diplomat or defendant may choose agentless wording; flag only if it deceives, and leave the decision to the writer.
- Keep a nominalization when it names something familiar or sums up the prior sentence. [[Keep useful nominalizations]]
- Legal/compliance wording where phrasing carries legal weight: preserve and ask.

## Procedure
1. Pair original and revision sentence by sentence (or by claim).
2. Run M1-M6; log each difference with level.
3. Check M7 and the quote/citation rule.
5. Return results in the output format defined by the meaning-checker agent (VERDICT preserved|issues; findings tagged block|ask|note = BLOCK|ASK USER|NOTE above).
5. Never auto-resolve an ASK; never silently accept a BLOCK.

## Vault links
[[L12 The Ethics of Style]] · [[Ethics of Style]] · [[Patterns - Ethical agency choices]] · [[Earn a reliable ethos by helping readers]] · [[Use clarity honestly rather than abandoning it]] · [[Doubt claims that new ideas require difficult prose]] · [[Reject the claim that difficulty improves thinking]] · [[Be as complex as necessary and no more]] · [[Calibrate hedges]] · [[Agent]] · [[Passive and Active]] · [[Nominalization]] · [[Clarity]]
