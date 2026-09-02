# Expect to throw work away

The book on Royal Road is the third draft. The first was a complete draft of book one, all three acts, written on the second day of the project and reclassified as groundwork on the fourth. The second included a full second act of some sixty-five scenes, drafted in a single push on 30 August and pulled the same evening. Neither will be read by anyone. Both were necessary, and the project's ability to discard them cheaply is a larger part of why the published book is any good than any individual rule about prose.

This is the part of the process people are least prepared for, because with a model producing text quickly it is tempting to treat every draft as an asset. Most of them are not. They are how you find out what the rules should have been.

## The two big discards

The first draft was written fast, before the voice rules had been tested against real output at length and before the dialogue work described on [the loop page](the-loop.md). By 27 August enough had been learned about what was wrong with it that fixing it in place was going to cost more than starting again, so it was declared scaffolding. The [chronicle entry](../chronicle/2026-08-27.md) records that this made a batch of earlier decisions about locked voice choices moot, which was a relief rather than a loss, since nothing published depended on them.

The second discard was sharper. On [30 August](../chronicle/2026-08-30.md) a whole act was drafted with the canon and editorial checks running as it went, and it passed them. Then the overlap checker, built the day before, showed that the new prose was too close to earlier rejected material. It read as recycled. The act was moved into a folder marked do not open, a rule about this specific kind of contamination went straight into the voice guide, and two scenes were redrafted from a clean brief that night to confirm the new process worked before anyone committed to redoing the rest.

## What the signs were

In both cases the draft was locally fine and globally wrong. Individual scenes read acceptably. The problem was a property of the whole: a voice that had drifted generic across the whole book, or an act whose phrasing echoed something that should have been forgotten. Checks that run scene by scene do not catch this. A reader reading a stretch cold does, and so does a tool that looks across the whole corpus, which is why the project's most consequential tools, the census and the overlap checker, are corpus-level rather than scene-level.

The other sign was a fix that kept growing. When repairing a draft turns into re-engineering scene after scene, and each repair reveals the next, the draft is telling you the underlying rules have changed since it was written.

## Making discarding cheap

Three things made the project's discards survivable. Drafts lived in version control, so throwing one away meant moving a directory, not losing anything. The knowledge extracted from a bad draft was already in the rule files by the time the draft was discarded, so the draft's value had been harvested. And the exemplars, the small set of pieces David actually liked, were kept separately from the drafts, so a discard never took the voice with it. The one time this went wrong, when early exemplar chapters were deleted as scaffolding on the first day, it took another day to diagnose the resulting voice drift and restore them.

## Steps you can take

1. Treat the first full draft of anything as a probe. Its purpose is to show you which of your rules are wrong. Write the rules it reveals into your files before you decide whether to keep it.
2. Keep exemplars separate from drafts, and under a rule that they are never deleted without a replacement being chosen first.
3. Every so often, read a long stretch cold, as a reader, and ask the corpus-level questions. Does this sound like one voice throughout? Does any of it feel familiar in a bad way? Have the model build tools that ask the same questions mechanically.
4. When you decide to discard, do it completely. Move the material out of anywhere a drafting session might read it, and if you need to check new work against it, do so through a tool that reads it from history rather than from the working tree. The [overlap checker page](../workflow/overlap-checking.md) explains why this matters.
5. Before redoing everything, redo a small piece under the new rules and check it. The project redrafted two scenes the night of the big discard for exactly this reason.
