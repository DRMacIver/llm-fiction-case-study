# Policing LLM tells: the linter and the language-police pass

Somewhere around a fifth of a day early in the project went into a fairly unglamorous activity: reading generated prose and cataloguing exactly what made it sound generated. The result, `notes/llm-tells.md`, lists over a dozen specific failure modes, ranging from surface habits (em-dash density, a narrow band of favourite vocabulary) to structural ones (prose that never rests, a maxim at the end of every paragraph, dialogue where every character is equally articulate, endings that land a crafted final beat instead of simply stopping). The deeper ones matter more and are harder to catch by eye, which is most of why so much tooling exists around this.

## The census method

The catalogue isn't a list of hunches. It came from a census of roughly 93,000 words of drafted prose, with 23 readers gathering specific "sounds off" lines, which were then checked against the accepted exemplar chapters to see whether the pattern was actually absent from the good prose or just less common. The resulting rules are ranked by how much each pattern contributed to the generated feel: a construction the project calls the "verdict clause," a sentence that states an event and then appends a clause judging it, turned out to be both the most frequent tell (around eleven per chapter in a drifted draft, four in the accepted seed) and one of the more damaging, because it does the reader's interpretive work for them.

Budgets from this census are measured per 1,000 words of prose, not per chapter, after an amendment found that a chapter-level budget could pass while a device was clustered densely in one section and absent elsewhere. A rule converted to a fixed per-chapter count would have quietly loosened as chapters grew from roughly 3,600 words to roughly 2,000 once the project moved to assembling chapters from finished scenes rather than drafting chapters directly.

## Three layers of checking

The actual hunt for tells in a given piece of text runs in three passes, each suited to a different kind of finding. A deterministic pass runs a Python linter, `tools/lint/prose_lint.py`, against a rules catalogue of just over a hundred entries in `tools/lint/rules.json`, covering everything that can be caught with a regular expression or a simple metric: banned words and phrases, the em-dash budget, negative-parallelism patterns like "not X, but Y." Anything this pass flags at its highest severity gets fixed mechanically, without needing a model's judgement at all.

What a regular expression can't catch, a fan-out of small model instances handles next: each rule group becomes a "lens," and one lightweight model call runs each lens against each file, returning candidate findings with a quoted passage, a line guess, and a reason. These findings are then handed to one larger model acting as a judge, which confirms or rejects each candidate, checks for anything the smaller passes missed, and does a final pass across every file together looking for the same defect recurring often enough to be worth turning into a new mechanical rule.

This structure exists because the two kinds of check are good at different things. A regex is fast, cheap, and exactly reliable on questions it can actually express, like counting em dashes. A model is the only thing that can judge whether a sentence's cleverness is earned by the scene it's in, but running a large model on everything is both more expensive and, on the project's internal benchmark of deliberately seeded defects, not obviously better at recall than a cheap first pass followed by a careful second one.

## Feeding back into the rules

New rules only enter the catalogue through David, reviewing findings the automated passes flag as candidates for a new mechanical rule. Rejected findings get logged as counter-examples in the rules file itself, so a plausible-sounding pattern that turned out to be a false positive doesn't get proposed again. This keeps the linter's catalogue a record of decisions actually made about this specific manuscript, rather than a generic style guide imported from elsewhere.
