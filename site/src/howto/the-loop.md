# The loop: how the back and forth actually goes

People who hear about this project most often ask some version of "but what do you actually say to it?" The transcripts are the full answer and they are long, so this page tries to describe the typical exchange and what distinguishes an exchange that moved the project forward from one that did not.

## A typical round

A round starts with David reading something. Usually that is a scene or a chapter the model has just drafted, sometimes it is a planning document or a piece of world-building. He reads it as a reader rather than a supervisor. The reports are short and specific, and they name the effect on the reader rather than the technique: the conversation feels artificial, this character is described by their function rather than shown doing anything, the reader no longer needs this explained by now.

The model's job at that point is not to apologise and fix the instance. It is to work out what general thing produced the instance, propose a rule or a check that would catch it in future, and then fix the instance under that rule. The rule goes into a file, written by the model. If the same class of problem comes back, David says so again and the model tightens the rule or builds a tool. Across the whole record the pattern is the same. David supplies the judgement in a sentence or two, and the model does the writing and keeps it maintained.

The clearest worked example is the dialogue work on [27 August](../chronicle/2026-08-27.md). David noticed that two characters, Edwin and one of his neighbours, had become too alike, so that their conversations blended together and sounded abrupt. The model proposed a test rather than a fix. Strip the speaker names from a page of dialogue and ask whether a reader can still tell who is talking. The first round scored badly. Over three more rounds, with concrete adjustments each time (shorter lines, a word cap in testing, each character forced to notice different props), attribution climbed until one late test assigned every line correctly. The result was a set of per-character voice rules written as countable constraints, and a standing rule that some characters do not listen perfectly, because a cast that always responds precisely to what was just said is uniform too.

The same shape shows up in smaller moments. When the model's first design for the story's farm-based magic system framed it as removing labour, David corrected it by hand to improving the return on labour, and that one sentence became a policy that shaped every later scene. When a first draft of the notes written in the voice of an in-story character leaned on invented lore, David pushed back, and the notes were reworked to use real-world farming facts only, guided by a document describing that character's voice.

## What makes feedback usable

Across the ten days of the project, the feedback that changed things had a few properties in common. It named a reader-level effect rather than a technique, so the model had room to find the actual cause, and it was specific enough that "fixed" meant something. Crucially it was delivered on real output rather than plans, since problems only turn up in output. And, last, it was allowed to become a rule, rather than being treated as a one-off correction.

Feedback that worked less well, where it appears in the transcripts, was aesthetic without a reason attached, or fixed the instance in a way the model could not generalise. The symptom is the same problem reappearing two scenes later. This is an impression from reading the record, not a count.

## The model's side of the loop

The transcripts show the model catching itself, more than once. On [31 August](../chronicle/2026-08-31.md) it noticed, mid-draft, that it had read some of the old contaminated scenes into its own context, stopped, and flagged the risk instead of continuing. On 28 August it found that its own method for scoring dialogue rounds was too dependent on who was scoring to support the comparisons already reported, and closed that line of work with a written note rather than dropping it quietly. Both happened because the project's rule files, written by the model at David's instruction, told it to stop and flag problems rather than smooth over them.

## Steps you can take

1. Read output, not plans, and report what you noticed as a reader. One or two specific observations per round beats a list of ten.
2. Ask the model what general thing caused the problem before asking it to fix the problem. Tell it to write the answer into a rules file. You do not write the file. You check that it says what you meant.
3. Check the fix on the next piece of output. If the problem recurs, tighten the rule or ask for a check that can run without you. The page on [turning feedback into checks](checks.md) covers that step.
4. Tell the model, in its standing instructions, that you want it to stop and say so when something is wrong, and that a retracted result is better than a quiet one. Then reward that when it happens.
