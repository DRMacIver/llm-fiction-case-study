# Voice devices to hunt in this site's prose

A catalogue for the voice pass over `site/src/{introduction,about}.md`,
`site/src/howto/*.md`, `site/src/workflow/*.md`, `site/src/chronicle/*.md`.
Sourced from `hegel-blog-post/notes/voice.md` §7 and its addenda, from
`autoroad/notes/llm-tells.md`, and from a read of `introduction.md`,
`howto/checks.md`, and `chronicle/2026-08-24.md`.

The site's narrator is the pipeline in the third person, openly LLM-written,
explaining a process to a reader — not David talking about himself. Devices
below are adapted to that register: drop anything that only makes sense for
first-person voice (footnote humour, swearing, "I" vs "we") and keep
everything about sentence- and paragraph-level shape, which transfers
directly.

Each entry: name, description, an example (drawn from the site where found,
otherwise constructed in the site's register), the plain alternative, and
whether it is **mechanically detectable** (a regex/metric could flag it,
even approximately) or **judgement-only**.

---

## Sentence-level devices

### 1. Triad-with-swerve / rule-of-three padding
Three items given rhetorical rhythm rather than because there are
substantively three things to distinguish.
- Example: "what the process looked like, what tooling it needed, what went wrong" (introduction.md — here it's fine, three genuinely different things; watch for the same shape used purely for cadence).
- Plain alternative: state as many items as there actually are, or fold into one sentence without the escalating list feel.
- **Mechanically detectable (approximate):** flag three comma/semicolon-separated clauses of similar length ending a sentence; needs eyeballing, high false-positive rate.

### 2. Negative parallelism ("not X, but Y" / "It wasn't X. It was Y.")
Defines something by first denying an alternative.
- Example (constructed): "This wasn't a formatting problem. It was a voice problem."
- Plain alternative: "The problem was in the voice, not the formatting" or just state the fact.
- **Mechanically detectable.**

### 3. Sentence-final verdict clause
An event stated, then a trailing "which was/which is/which cost/which took" clause grading it.
- Example: "which is most of why it is worth reading" (introduction.md); "which is most of why" (introduction.md, workflow line).
- Plain alternative: state the judgement as its own sentence, or cut it if it isn't adding information.
- **Mechanically detectable** for the closed set of trailing-which patterns; open set needs eyeballing.

### 4. Meta-dramatising importance / interest
Announcing that something is significant, load-bearing, or interesting instead of showing it.
- Example (constructed): "This is the part of the process that mattered most."
- Plain alternative: cut the announcement, let the following sentence carry the weight on its own.
- **Mechanically detectable** for stock phrases ("load-bearing", "does the heavy lifting", "worth noting/noticing", "the interesting part is").

### 5. "Worth noting" / "worth noticing" / "notably" / "importantly"
Importance-narration in miniature — flags a fact as significant rather than making it significant by context.
- Example (constructed): "It's worth noting that the checker caught 206 mismatches."
- Plain alternative: "The checker caught 206 mismatches" — let the number do the work.
- **Mechanically detectable.**

### 6. "In the plain sense"
A hedge-qualifier that gestures at precision without adding it — asserts a word is being used non-metaphorically, as if forestalling an objection nobody raised.
- Example: "That is hallucination in the plain sense" (howto/checks.md).
- Plain alternative: "That is hallucination — the model asserted something false" or just "That is hallucination."
- **Mechanically detectable** (fixed phrase).

### 7. "Which is most of why"
A causal hedge-clause construction that sounds considered but rarely earns its qualification ("most of").
- Example: "which is most of why it is worth reading" / "which is most of why" (introduction.md, two instances).
- Plain alternative: "which is why", or state the reason plainly without the clause.
- **Mechanically detectable** (fixed phrase).

### 8. Hedge-stacking
Multiple diffuse qualifiers piled in one sentence, draining it of a definite claim.
- Example (constructed): "It could be argued that, to some extent, this was probably the main cause."
- Plain alternative: pick one hedge, attach it to a still-definite claim.
- **Mechanically detectable** (regex for 2+ hedge words in one sentence).

### 9. "Here is what / here's the thing"
Staged-reveal framing that announces a disclosure is coming rather than just disclosing it.
- Example (constructed): "Here is what actually happened next."
- Plain alternative: state the thing.
- **Mechanically detectable.**

### 10. Copula avoidance / marketing verbs
"Serves as", "stands as", "boasts", "features" where "is"/"has" would do.
- Example (constructed): "The rules file serves as the project's memory."
- Plain alternative: "The rules file is the project's memory."
- **Mechanically detectable.**

### 11. Em dash as connective tissue
Reached for reflexively instead of parentheses, colons, or a new sentence.
- Plain alternative: recast with a colon, parenthesis, or a full stop.
- **Mechanically detectable** (count + flag every instance for review).

### 12. Semicolons
Report-register punctuation, rare in the target voice.
- Plain alternative: two sentences, or join with "and"/"but".
- **Mechanically detectable.**

### 13. Dramatised absence of signal
"Silently", "never announced itself", "quietly collapsed" used for drama rather than fact.
- Example (constructed): "The bug never announced itself."
- Plain alternative: "Nobody noticed the bug until..." — state what actually happened.
- **Mechanically detectable** (closed vocabulary list).

### 14. "Earn its/their keep" and cousins
Stock idiom of justification.
- Example (constructed): "The linter earns its keep on the vocabulary rules alone."
- Plain alternative: say plainly why the thing is useful, or just present it.
- **Mechanically detectable.**

### 15. Pre-empting the reader's reaction
Telling the reader how a fact will land before giving it.
- Example (constructed): "That number is less reassuring than it sounds:"
- Plain alternative: give the reason instead of the forecast.
- **Judgement-only** (hard to pattern-match reliably; a few stock openers like "less X than it sounds" are catchable).

### 16. The gesture at meaning
A sentence shaped like it's saying something with nothing concrete inside it ("that was the whole shape of it", "which meant something").
- Example (constructed): "That was, in its way, the whole shape of the problem."
- Plain alternative: say what the shape actually was, or cut the sentence.
- **Judgement-only.**

---

## Paragraph- and structure-level devices

### 17. Paragraph opens by announcing its point
The first sentence states the paragraph's thesis in general terms before any concrete material; the rest of the paragraph then illustrates it.
- Example: "There is a point in any project like this where you notice you have given the same note three times." (howto/checks.md, opening line — sets up the abstraction before any specific instance.)
- Plain alternative: open on the concrete instance, let the generalisation follow or stay implicit.
- **Judgement-only** (structural, not pattern-matchable).

### 18. Closing sentence recontextualises too neatly
A paragraph or section's last sentence reframes everything before it into a tidy, quotable lesson.
- Example (constructed): "The problem was never the prose. It was what the notes said about the prose."
- Plain alternative: let the section end on its last concrete fact; cut the reframe.
- **Judgement-only.**

### 19. "This is the part that..."
A sentence that flags significance of an upcoming or just-given passage rather than the passage carrying it on its own (specific case of device 4, common enough in explanatory writing to name separately).
- Example (constructed): "This is the part of the process that took the longest to get right."
- Plain alternative: cut it; let the length or detail of the surrounding explanation show it.
- **Mechanically detectable** (fixed phrase family: "this is the part", "this is where").

### 20. Bold-lede summary line
A bolded one-sentence headline opening a section, functioning as an abstract before the prose (seen at the top of chronicle entries).
- Example: "**The premise was set and a narrator's voice was built from scratch, twice.**" (chronicle/2026-08-24.md)
- Note: this may be an intentional site convention for chronicle pages rather than a tell — check with the human before flagging it as a defect; the voice guide's rule against bold is about bold used as an emphasis/scanning aid inside running prose, which is a different case from a designed section header.
- **Mechanically detectable** (regex for bold spanning a whole sentence at a section's start), but treat findings as REVIEW not FAIL given the open question above.

### 21. Parenthetical list of three
A parenthetical aside itself padded to three items for rhythm rather than because three specific things are being distinguished.
- Example: "(particular hedging words, a fondness for arithmetic-flavoured metaphors, over-explaining)" (chronicle/2026-08-24.md — here genuinely three distinct habits, a clean case; watch for the same shape used to pad).
- Plain alternative: list only the items that matter, or say "for example, X" with one.
- **Mechanically detectable (approximate):** parenthetical with two commas and no "and"-conjunction before the last item; needs eyeballing.

### 22. Over-signposting
Announcing the structure of the explanation instead of just giving it ("Three things go wrong", "There are two reasons for this").
- Example (constructed): "There are three reasons the linter caught this."
- Plain alternative: give the reasons; let the count be implicit or stated only if genuinely useful to the reader.
- **Mechanically detectable** (numeral + "reasons"/"things"/"ways" pattern).

### 23. Self-quotation callback
"As mentioned above" / "as noted earlier" used as connective tissue rather than because the reader needs the reminder.
- Plain alternative: cut it, or repeat the fact briefly instead of pointing back at the earlier sentence.
- **Mechanically detectable** (fixed phrases).

### 24. Relentless both-sides balance
Every claim immediately qualified with an opposing consideration, so nothing is stated flatly.
- **Judgement-only.**

### 25. Report-register: verbless fragments and spec-sheet parentheticals
Measurement or process description dropping into lab-report grammar: fragments without a finite verb, or parenthetical numeric asides doing what a clause should.
- Example (constructed): "Ran the checker. 206 mismatches, 110 fabricated."
- Plain alternative: give it a subject and a finite verb: "The checker's first run found 206 mismatches, of which 110 were fabricated."
- **Mechanically detectable (approximate):** sentence-initial past-participle fragment lacking a following finite verb.

### 26. Noun-compound packing
Stacked attributive nouns / ad-hoc hyphenated compounds where a prepositional phrase would be plainer.
- Example (constructed): "a voice-drift diagnosis pass."
- Plain alternative: "a pass to diagnose the voice drift."
- **Mechanically detectable (approximate):** count of hyphenated compounds per 1000 words, flagged as INFO not FAIL/REVIEW per-instance (too many legitimate technical compounds in this domain — "fan-out", "voice-drift" as an established site term — to ban outright).

### 27. Adverb-heavy rate
High density of -ly adverbs propping up otherwise plain verbs, a mild but real machine-prose signal.
- **Mechanically detectable** (rate per 1000 words, INFO tier).

### 28. Local coinage ridden too hard
A metaphor or pet phrase invented once and then used repeatedly as running vocabulary in place of plain language.
- **Judgement-only** (needs corpus comparison across the whole site; flag candidates by counting repeated multi-word phrases, judge manually).

---

## Vocabulary (zero-tolerance / review)

Combined from both source catalogues, filtered to items plausible in
expository non-fiction about a software/writing project (dropped fiction-only
items like "hydrogen jukebox" abstraction-jamming, dialogue ecosystem, etc.):

**Zero-tolerance (FAIL):** delve (into), tapestry, testament to, in today's,
navigate the ...landscape, game-changer/game-changing, seamless(ly),
elevate your, key takeaways, earn(s)/earning its/their keep, announce(d)
itself, intricate, pivotal, underscore(s/d) (verb), nestled, vibrant,
profound(ly), myriad (adjective use), serves as / stands as / boasts /
features (marketing-verb copula avoidance).

**Review (sometimes fine):** leverage (verb), robust, crucial, notably,
importantly, it's worth noting/noticing, load-bearing, does the heavy
lifting, arguably, silently, honest [noun] ("an honest account", "an
honest list" — narrator-approval tic), ordinary (as loaded judgement word).

---

## Site-specific notes

- The narrator here is impersonal (the pipeline / the project), so several
  first-person-specific tells from voice.md (I/we ratio, footnote humour,
  self-deprecation) don't transfer directly — but a third-person equivalent
  of over-styling still applies: watch for the narrator performing
  personality it doesn't have standing to perform (jokes at nobody's
  expense, dramatic irony about "the project" as if it were a character).
- The site's own style already has real, deliberate structure (bold lede
  lines on chronicle pages, cross-links between chronicle and workflow) —
  don't flag site conventions as tells; flag only where a *device* rather
  than a *convention* is doing the work.
