# Lens: Cohesion, coherence & emphasis
**Question this lens asks:** Does each sentence start on what the reader already knows and end on what is new and worth stressing, and do the subjects across the paragraph stay on a few consistent topics?
**Level:** sentence-to-sentence and paragraph · **Quick mode:** CE1 (old-new pairs), CE3 (topic string from `topic_string`), CE5 (stress at sentence ends), CE7 (faked connectors). Run CE2, CE4, CE6, CE8-CE11 only in full mode.
**Mechanical hints:** (textstats signals; they only point, they never prove)
- `topic_string`: read the first-7-word openings of consecutive sentences. Unrelated, abstract, long, or randomly shifting openers point to CE3/CE4. Identical openers across many sentences point to CE9 (usually fine).
- `PASS`: a passive candidate is often a deliberate old-first move. Check it against CE1 before flagging it.
- `META`: metadiscourse at the end of a sentence points to CE5/CE6. At the front it points to CE4 (throat-clearing).
- `INTRO`: a long opener before the subject points to CE4.
- `EXPL` (there is / it is...that): flag only if the placeholder hides the topic (CE3). Keep it when it moves new material to the end (CE6).
- Missing signals: old/new cannot be measured. Judge it by comparing the end of sentence n with the start of sentence n+1. The author's own text always feels old to the author, so check each pair mechanically.

## Priority rule
When clarity principles clash, old-before-new beats characters-as-subjects and actions-as-verbs. Cohesion of the passage outranks the "clarity" of a single sentence in isolation. The three usually agree; apply the rule only when they clash.

## Checks (in order of payoff)

### CE1 · Old before new (pair handoff)
- **Symptom:** For each adjacent pair, sentence n+1 opens with something sentence n never mentioned or implied (a new subject out of nowhere). The text feels choppy. Backward-pointing words (*this, another, such, these*) sit late in the sentence.
- **Fix:**
  1. Find what sentence n ends with.
  2. Make that item, or a familiar relative of it, the subject or opener of n+1.
  3. Put the new, long, technical material at the end of n+1.
  4. Flip with a passive or an inversion if needed.
  5. Check that the new ending sets up sentence n+2.
  6. Move reference words to the start (*Another issue we must consider is how to calculate credits...*).
- **✗/✓:** ✗ ...scientists studying black holes in space. The collapse of a dead star into a point no larger than a marble creates a black hole. → ✓ ...black holes in space. A black hole is created by the collapse of a dead star into a point perhaps no larger than a marble.
- **Leave it when:** the sentence deliberately opens with new material for emphasis; the passage genuinely changes direction; the sentence opens a paragraph or section (nothing precedes it); the old-first form would need a worse sentence, such as a passive that hides a needed agent in high-stakes text (see Conflicts).
- **Vault:** [[Begin sentences with old information]] · [[End sentences with new information]] · [[Link the end of one sentence to the start of the next]] · [[Put reference signals at the start of the sentence]] · [[Favor cohesion over single-sentence clarity]] · [[Old-new test]] · [[Patterns - Old before new]]

### CE2 · Passive to put old information first
- **Symptom:** An active sentence has a new subject and an object or agent that was just mentioned. Fix this only when it also fails CE1.
- **Fix:** Make the old element the subject (passive, or the converse verb). Put the new element at the end, in a *by* phrase if it is the agent. Keep the agent if it is new or informative.
- **✗/✓:** ✗ Some claim that our genes influence aspects of behavior we think are learned. Our genes, for example, seem to determine... → ✓ Some claim that aspects of behavior we think are learned are influenced by our genes. Our genes, for example, seem to determine...
- **Leave it when:** the active sentence already starts old (stay active, which is the default); the agent is the important new information and the passive would bury it; the passive hides responsibility in a high-stakes text (use the other lens's agency check).
- **Vault:** [[Use the passive to put old information first]] · [[Use the passive to put familiar information first]] · [[Choose active or passive by three questions]] · [[Patterns - Old before new]]

### CE3 · Subjects name topics; topic string short and consistent
- **Symptom:** The first 7 words of a paragraph's sentences name many unrelated or abstract things. The subject is a placeholder (*It is impossible for your claim to be proved*) or the topic hides in a prepositional phrase (*In regard to this question, I believe...*). The passage feels unfocused even when each sentence is clear.
- **Fix:**
  1. List the topic-string openers.
  2. Pick 2-3 main topics (the characters, real or abstract).
  3. Make them the subjects of most sentences.
  4. Move other material out of the subject slot.
  5. Confirm each topic is familiar to the reader.
  6. If a topic is absent for several sentences, ask whether the passage has drifted.
- **✗/✓:** ✗ Consistent ideas toward the beginnings of sentences help readers understand what a passage is about. → ✓ Readers understand what a passage is generally about when they see consistent ideas toward the beginnings of sentences.
- **Leave it when:** "most, not all" sentences; a fronted object is deliberate (*Such results no one could have predicted*); the passage is a list or catalog where the topics change by design; a subject is a short set-up for a clear end (a short *There are three reasons...* before a list).
- **Vault:** [[Make subjects name topics]] · [[Keep topic strings short and consistent]] · [[Topic string test]] · [[Patterns - Topic strings and openers]]

### CE4 · Throat-clearing before the subject
- **Symptom:** Several sentences in a row stack transition + attitude metadiscourse + time/place phrase before the subject (*And, therefore, it is important to note that, in Eastern states since 1980, acid rain...*). `INTRO` fires.
- **Fix:** Cut the metadiscourse. Keep one connector only if it names a real relation. Move time and place phrases behind the subject, or trim them. Get to the topic quickly.
- **✗/✓:** ✗ And, therefore, it is important to note that, in Eastern states since 1980, acid rain has become a serious problem. → ✓ Since 1980, therefore, acid rain has become a serious problem in the Eastern states.
- **Leave it when:** one framing opener appears occasionally (a time or condition phrase that orients the reader is fine); an introductory phrase carries old information that links back to the previous sentence; the opener is short and simple. The harm is the pile-up across several sentences, not a single opener.
- **Vault:** [[Clear throat-clearing before the subject]] · [[Open sentences with short simple elements]] · [[Throat-clearing test]] · [[Patterns - Topic strings and openers]]

### CE5 · Stress test on sentence endings
- **Symptom:** The last 3-4 words are an attribution (*according to scientists*), a hedge (*for the most part*), anticlimactic metadiscourse (*it must be remembered*), a redundant tail, or a repeated word. The point sits in the middle.
- **Fix:**
  1. Identify the words the sentence exists to deliver.
  2. Move peripheral material (hedges, attributions, metadiscourse) to the front or inside, so that the point ends the sentence.
  3. Move new or technical information right (CE6).
  4. Trim redundant tails (CE6).
- **✗/✓:** ✗ The data offered to prove ESP are weak, for the most part. → ✓ For the most part, the data offered to prove ESP are weak.
- **Leave it when:** the author wants a different word stressed (the choice depends on purpose; the stress may fall on the blamed party); a closing hedge or qualification is the point, as in an intentional afterthought; the shifted material would create a throat-clearing pile-up (CE4). Do not move a hedge so far left that it modifies the wrong clause.
- **Vault:** [[Put the words you want emphasized in stress position]] · [[Shift peripheral ideas to the left]] · [[Stress test]] · [[Patterns - Moving material to the end]]

### CE6 · Shift new, complex or technical material to the end
- **Symptom:** A long or new element fills the subject while a short familiar linking phrase trails (*Questions about the ethics of ... are more difficult*). A technical term appears at the start of its sentence, or is used without introduction. A tail repeats an earlier idea.
- **Fix:**
  1. Trim a redundant tail first.
  2. Invert (*More difficult are questions about...*).
  3. Use a *there is*, *what... is*, or *it... that* shift to push the heavy element into stress.
  4. Introduce a technical term at the end of a sentence, spell out implicit steps, then reuse the term as old information in the next opener.
  5. Use *not only X, but also Y* to stress Y.
- **✗/✓:** ✗ We need a monetary policy that would end fluctuations in money supply, unemployment, and inflation. → ✓ What we need is a monetary policy that would end fluctuations in money supply, unemployment, and inflation.
- **Leave it when:** the tail is not truly redundant (the author may need what the trim removes); the shift would produce a flabby *there are...* or *it is...* in text that is already full of them (then keep the plain form); the sentence is already short and ends on the key word; the *not only-but* pair is not parallel; the writer's term is already familiar, so no introduction is needed.
- **Vault:** [[End sentences with new information]] · [[Shift new information to the right]] · [[Trim the end of the sentence]] · [[Introduce technical terms in stress position]] · [[Use there, what, and it shifts to control stress]] · [[Use not only-but to stress the second element]] · [[Patterns - Moving material to the end]]

### CE7 · Faked connection (conjunction audit)
- **Symptom:** More than a few *therefore, thus, hence, however, indeed, moreover, also, another, consequently* per page, where you cannot state the logical relation. *And/also/another* just mean "one more thing". Most likely where the ideas were struggling.
- **Fix:**
  1. For each connector, name the relation (contrast, consequence, conclusion).
  2. If it holds, keep it.
  3. If not, delete it and let the topic string and old-new handoff carry the link.
  4. If the logic is missing, fix the argument or flag it. Do not paper over it.
- **✗/✓:** ✗ ...influences his popularity. Therefore, it should report on the president objectively. Both reporters and the president are human, however... Also, people act differently in public... Hence, to understand a person... → ✓ (cut the bluffs; make the sentences follow from each other through repeated topics and old-new links)
- **Leave it when:** the relation is real (*but* marks a true contrast; *therefore* marks a conclusion). Experienced writers use connectors, but the logic is in the ideas. Do not strip all transitions, and do not delete a connector that the reader needs to see a turn.
- **Vault:** [[Do not fake coherence with conjunctions]] · [[Faked connection test]] · [[Link revised clauses with precise connectors]]

### CE8 · Opening sentence announces themes in stress; thread them
- **Symptom:** A paragraph of more than 5-6 sentences has no identifiable framing sentence. The key concept appears only late, or the opener's last words do not read like a title for the paragraph. Later sentences do not repeat any cluster of related words.
- **Fix:**
  1. Write or revise the framing sentence so that its last words name the 2-3 organizing concepts.
  2. Repeat those concepts through the body. Concepts that are characters become subjects; others recur as nouns, verbs, or adjectives.
  3. If sentence topics are random, fix CE3 first.
- **✗/✓:** ✗ Great strides in the early and accurate diagnosis of Alzheimer's disease have been made in recent years. → ✓ In recent years, researchers have made great strides in the early and accurate diagnosis of Alzheimer's disease, but those diagnoses have raised a new problem about informing those most at risk who show no symptoms of it.
- **Leave it when:** the paragraph is short (2-3 sentences) or is a transition or intro bridge; the paragraph is a list or a step in a procedure; the point is deliberately delayed (a narrative or a suspense build). Do not stuff extra themes into the opener until it sprawls.
- **Vault:** [[Announce key themes in the stress of the opening sentence]] · [[Thread themes through a passage]] · [[Opening sentence test]]

### CE9 · Do not vary subjects for variety
- **Symptom:** (Reverse check, to stop bad edits.) An editor or style rule tells you to change repeated subjects or openers just for variety. This diagnoses a wrong fix, not a flaw in the text.
- **Fix:** Keep the repeated topic. Vary wording only if the same words recur in the same position to an excessive degree (*"Moral climate"... Moral climate... moral climate...*): swap in *this climate*, a near synonym, or a related term.
- **✗/✓:** ✗ "Moral climate" is created... Moral climate results... moral climate acts... A moral climate encourages... → ✓ "Moral climate" is created... This climate results... In this light, morality acts... A moral climate encourages...
- **Leave it when:** (inverse) the repetition is truly mechanical and unbroken, as above. Otherwise do not touch it.
- **Vault:** [[Do not vary subjects for variety]] · [[Keep topic strings short and consistent]]

### CE10 · One point of view
- **Symptom:** The subjects alternate between two parties or characters (*the Allies... Germany... they... its...*) with no reason, and pronouns become ambiguous.
- **Fix:** Pick the viewpoint character. Keep it as the subject across the passage, and use passives or converse verbs to hold it there.
- **✗/✓:** ✗ The Allies had defeated Germany. Its borders had been breached, and they were bombing it... Germany was not so devastated, however, that the Allies... → ✓ (German view) By early 1945, Germany had essentially been defeated. Its borders had been breached, and it was being bombed around the clock.
- **Leave it when:** the story genuinely changes focus; a contrast or negotiation needs both parties as subjects; a dialogue or an argument alternates by nature.
- **Vault:** [[Hold one point of view across sentences]] · [[Make subjects name topics]]

### CE11 · Repeated word at the end
- **Symptom:** The last word repeats a word used a few words earlier, and the voice drops (a fine point).
- **Fix:** Use a pronoun or ellipsis, rewrite, or delete the repeat.
- **✗/✓:** ✗ ...but more often you cannot represent it in that kind of sentence. → ✓ ...but more often you cannot.
- **Leave it when:** the repetition is a deliberate rhetorical echo (the elegance lens covers it); a pronoun would be ambiguous; a technical or legal term must stay exact.
- **Vault:** [[Avoid ending a sentence on a repeated word]] · [[Stress test]]

## Rewrite patterns (cheat table)
| shape before | shape after |
|---|---|
| New noun phrase as subject right after an old noun at the end of the previous sentence | Old noun as subject, passive verb, new material at the end |
| *How to X is another issue we must consider.* | *Another issue we must consider is how to X.* |
| *The number of dead in the Civil War exceeded all other wars.* | *Of all the wars in American history, none has exceeded the Civil War in the number of dead.* |
| *Only X will afford it if this trend continues.* | *If this trend continues, it will be affordable only by X.* |
| *It is impossible for your claim to be proved.* | *Your claim cannot be proved.* |
| *In regard to this question, I believe more research is needed.* | *This question needs more research.* |
| *And, therefore, it is important to note that, in [place] since [date], X...* | *Since [date], therefore, X ... in [place].* |
| *...would disappear, according to scientists.* | *According to scientists, ... would disappear.* |
| *The data are weak, for the most part.* | *For the most part, the data are weak.* |
| *X are getting scarcer, it must be remembered.* | *It must be remembered that X are getting scarcer.* |
| *Questions about [long thing] are more difficult.* | *More difficult are questions about [long thing].* |
| *We need [long thing].* | *What we need is [long thing].* |
| *That X would happen once seemed inevitable.* | *It once seemed inevitable that X would happen.* |
| *Several devices let you...* | *There are several devices that let you...* |
| *X and Y* (Y is the point) | *not only X, but also Y* |
| *...control our social behavior in the way we act in situations we are in every day.* | *...control our social behavior.* |
| *...cannot represent it in that kind of sentence.* | *...cannot.* |
| Framing sentence ends on a trivial word | Framing sentence ends on the 2-3 theme words that recur below |

## Conflicts with other lenses
- **Cohesion vs. active voice / characters as subjects.** The book ranks old-before-new first. Keep the character subject when it is also old. Switch to a passive only when the old element is the object or the new element is the subject.
- **Cohesion vs. hidden agents (ethics lens).** A passive that serves old-before-new must not hide an agent the reader needs (a person responsible, in high-stakes text). Name the actor in a *by* phrase, or choose a different old-first form.
- **Old-first passive vs. nominalizations.** Do not fix an old-first problem by turning a good verb into a nominalization. Keep verbs as actions, and move the order only.
- **Stress vs. concision.** Trimming (CE6) is also a concision move. Trim only if the tail repeats; do not cut a qualification the claim needs (concision and hedge-calibration lenses own this).
- **Left-shifted hedges vs. throat-clearing.** Moving metadiscourse from the end to the front (CE5) can create a pile-up (CE4). Prefer cutting it; if it must stay, keep it short.
- **Stress vs. sentence shape.** Placing heavy material last fits the shape lens (short opener, long end). If it produces a trailing chain of clauses, fix the sprawl there.
- **Topic consistency vs. elegance/variety.** Repeating the topic beats varying it for variety. Elegant echoes (grace lens) are deliberate and are exempt from CE11.
- **Placeholder subjects.** *There is* and *it is...that* are flagged by the characters lens as empty. Here they are allowed when they shift new material into stress (CE6). Decide by where the new information ends up.

## Over-correction traps
- Do not apply old-first to every sentence. The first sentence of a paragraph or section has nothing before it, and a deliberately new opener can create emphasis.
- Do not turn every active sentence into a passive. Flip only when the previous sentence's ending shows the flip is needed.
- Do not delete all transitions as "faked". A true *but* or *therefore* is part of the logic (CE7).
- Do not force sentence variety, and do not impose it as a fix. Repeated topics are a strength (CE9).
- Do not force a single topic across the whole text. Topics change where the subject changes, and a catalog or a procedure will not have a short topic string.
- Do not move every hedge or attribution to the front. A sentence needing several fronted qualifiers becomes throat-clearing.
- Do not add *what is*, *it is...that*, or *there are* shifts to sentences that are already clear. Use them only when stress needs them.
- Do not trim a tail that carries a distinction the author needs.
- Do not insert theme sentences into short paragraphs, or insert a framing sentence that only announces ("This paragraph discusses...").
- Do not judge old/new from your own sense of the text. If you cannot tell what the reader knows, test the pair against the previous sentence's actual words.
- Do not rewrite a passage to fix flow if the real problem is missing logic. Report it to the author.
