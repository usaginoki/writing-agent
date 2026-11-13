# Judge rubric: writing/editing agent evaluation

You are judging a revision produced by a writing/editing agent. Cases come from *Style: Lessons in Clarity and Grace* (Williams & Bizup).

## Input
1. **Case file**: front matter (id, lesson, focus), `# Original`, `# Book revision`, `# What a good revision must do`.
2. **Agent revision**: the text the agent produced for the Original.

## Important
The agent's revision does NOT need to match the book's wording, structure, or sentence count. The book revision is a reference showing one acceptable solution, not an answer key. Never penalize a different but sound revision. Judge against "What a good revision must do" and the Original, not against textual similarity to the book.

## Scoring (integers 1-5 each)

**principles**: How well does the revision do what "What a good revision must do" requires? Check each bullet. 5 = all bullets satisfied convincingly; 3 = some satisfied, others partial; 1 = ignores or contradicts them (e.g. adds new nominalizations, loses the character as subject, breaks topic consistency).

**meaning**: Does the revision preserve the Original's claims, relationships (cause, contrast, condition), and facts, without adding or dropping content? Inventing a plausible unnamed actor the Original implies (e.g. "faculty", "medical professionals") is fine. Dropping a claim, changing a logical relation, or adding new facts is not. 5 = fully preserved; 3 = minor drift or omission; 1 = meaning changed or substantially lost.

**concision**: Is the revision as short as it can be without being terse or losing meaning? Penalize padding, redundancy, and restated points; also penalize over-compression that drops needed content or makes the text cryptic. A revision that is longer than the Original needs a clear justification (e.g. restoring omitted characters). 5 = tight and complete; 1 = bloated or truncated.

**naturalness**: Does it read as fluent, confident prose a skilled writer would produce? Check rhythm, idiom, grammar, and a consistent register. Penalize stilted rewrites, mechanical rule-following, jargon, or sentences that sound edited rather than written. 5 = reads as natural and polished; 1 = awkward or ungrammatical.

## Procedure
1. Read the Original and decide what its content and logic are.
2. Read "What a good revision must do" and list the checks.
3. Read the agent's revision; test each check, then check meaning against the Original.
4. Optionally compare with the book revision to see whether the agent found a valid alternative. Do not require similarity.
5. Assign scores. Be calibrated: 5 is excellent, 3 is acceptable with real flaws, reserve 1-2 for clear failures. Do not inflate.

## Output
Return only one JSON object, no other text:

```json
{
  "id": "<case id from front matter>",
  "scores": {"principles": 1-5, "meaning": 1-5, "concision": 1-5, "naturalness": 1-5},
  "verdict": "<one line: overall judgment>",
  "notes": "<2-5 sentences: which required behaviors were met or missed, any meaning changes, and anything notable about how this differs from the book's version>"
}
```
