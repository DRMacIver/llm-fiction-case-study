# Turn recurring feedback into checks

There is a point in any project like this where you notice you have given the same note three times. The project's answer, every time this happened, was to stop giving the note and build something that gives it instead. The something ranged from a line in a list of banned words to a script that reads git history. A check does not have to be sophisticated to be worth having.

## The ladder of checks

At the bottom is a plain list. The project's catalogue of machine-prose habits started as a document of observations and grew a rules file of just over a hundred entries: banned words and phrases, a budget for em dashes, a pattern for the "not X, but Y" construction. Anything a regular expression can express is caught by a small Python linter that runs in seconds and never disagrees with itself. This caught a great deal. It is also the least glamorous thing on this site and probably the easiest to copy, since the model wrote and maintained the linter on request.

One rung up is measurement. The project counted how often certain devices appeared per thousand words of prose, and compared the count in a drifted draft against the count in the accepted exemplars. That is how it found that a construction it called the "verdict clause", an event followed by a clause judging it, ran at roughly eleven per chapter in drifted prose and four in good prose. That gave the aesthetic complaint a number and a target, so the target could be checked automatically. Budgets were later converted from per-chapter counts to rates per thousand words, because chapters changed length and a fixed count would have loosened silently.

Above that is model-based review, and it needs a structure. For anything a regex cannot judge, the project fans out small, cheap model calls, one per rule group per file, each returning candidate findings with a quoted passage and a reason. A larger model then judges the candidates, confirms or rejects each, and looks across all files for the same defect recurring often enough to become a new mechanical rule. This shape, fanning candidates out and then having one call judge them, recurs throughout the project, and the [linting page](../workflow/llm-tells-and-linting.md) explains why it beat one large model doing the whole pass.

At the top are checks that look outside the prose. The [citation checker](../chronicle/2026-08-28.md) verifies that every quotation in the project's canon (its record of established facts) and planning files actually appears in the chapter it claims to come from. Its first run found 206 mismatches. Of those, 110 were quotations that had never been written, invented by the model about its own earlier work. Rereading the chapters would not have caught this, because the chapters themselves were unaffected: the fabricated quotations lived only in the notes about them. The [overlap checker](../workflow/overlap-checking.md) looks for runs of eight or more words shared between a new scene and drafts that were discarded, pulling the old drafts from git history so that no session ever has them in its working tree.

## What to check

Looking at what the project's checks actually caught, they fall into a few families. The linter and census handle prose habits. The canon checks handle consistency with what has already been established scene by scene, and a [workflow](../workflow/consistency-workflows.md) handles it across a whole book. The citation checker handles fabrication, where the model asserts something about its own earlier work that is not true. The overlap checker handles contamination, where new work leans on old rejected work. Any long generative project will hit all four, and the last two are the ones that seem least anticipated.

## Steps you can take

1. Have the model keep a file of banned words and constructions from the first day. Every time you object to a phrase, tell it to add the phrase, and have it write and maintain a script that flags them. In this project that file and script were the model's work throughout, done on the instructions of the project's author, David MacIver.
2. When a complaint is about frequency ("too many of these"), ask for a number. Have the model count the device in a piece you like and in a piece you do not, and set the target from the one you like.
3. When a check needs judgement, structure it. Ask for several narrow reviewers, each with one question, feeding one reviewer who decides. Do not ask one call to find everything.
4. Check the notes, not just the prose. Anything the model says about its own earlier output, including quotations, summaries and claims about what a chapter established, should be verifiable mechanically, and you should periodically tell the model to verify it.
5. Let rules enter the checker only with your say-so, even though the model does the editing. The project logged rejected findings as counter-examples in the rules file, so a plausible false positive would not be proposed again.
