# The loop: how the back and forth actually goes

The question people most often asked was some version of "but what do you actually say to it?" The transcripts are the full answer and they are long, so this page tries to describe the typical exchange and what distinguishes an exchange that moved the project forward from one that did not.

## A typical round

A round starts with David reading something. Usually that is a scene or a chapter the model has just drafted, sometimes it is a planning document or a piece of world-building. He reads it as a reader, not as a supervisor, and reports what he noticed. The reports are short and specific, and they name the effect on the reader rather than the technique: the conversation feels artificial, this character is described by their function rather than shown doing anything, this exposition should be past needing by now.

The model's job at that point is not to apologise and fix the instance. It is to work out what general thing produced the instance, propose a rule or a check that would catch it in future, and then fix the instance under that rule. The rule goes into a file. If the same class of problem comes back, the rule gets tightened or a tool gets built.

The clearest worked example is the dialogue work on [27 August](../chronicle/2026-08-27.md). David noticed that characters' conversations felt off: too many clever dangling lines, questions answered with non-answers, everyone in the same aphoristic register. The model proposed a test rather than a fix. Strip the speaker names from a page of dialogue and ask whether a reader can still tell who is talking. The first round scored badly. Over three more rounds, with concrete adjustments each time (shorter lines, a word cap in testing, each character forced to notice different props), attribution climbed until one late test assigned every line correctly. The output was not a better page of dialogue. It was a set of per-character voice rules written as countable constraints, and a standing rule that some characters do not listen perfectly, because a cast that always responds precisely to what was just said is another form of uniformity.

The same shape shows up in smaller moments. When the model's first design for farm magic framed it as removing labour, David corrected it by hand to improving the return on labour, and that one sentence became a policy that shaped every later scene. When a first draft of the in-story author's notes leaned on invented lore, David pushed back, and the notes were reworked to use real-world farming facts only, with a persona document to keep them consistent.

## What makes feedback usable

Looking across the ten days, the feedback that changed things had a few properties in common. It named a reader-level effect rather than a technique, which left the model room to find the actual cause. It was specific enough to be checked, so that "fixed" meant something. It was delivered on real output, not on plans, because the model's plans are always plausible and its output is where the problems are. And it was allowed to become a rule. David's role was described in the project's own notes as adversarial in a useful sense: largely to catch places where the model's quality bar had slipped.

Feedback that did not work as well tended to be aesthetic without a reason attached, or to fix the instance in a way the model could not generalise. There are examples of both in the transcripts, and the recurring symptom is the same problem reappearing two scenes later.

## The model's side of the loop

Something worth noticing in the transcripts is how often the model catches itself. On [31 August](../chronicle/2026-08-31.md) it noticed, mid-draft, that it had read some of the old contaminated scenes into its own context, stopped, and flagged the risk instead of continuing. On 28 August it found that its own method for scoring dialogue rounds was too dependent on who was scoring to support the comparisons already reported, and closed that line of work with a written note rather than dropping it quietly. Neither of those happened by accident. Both followed periods where David had made clear that he wanted problems surfaced rather than smoothed over, and the project's rule files said so in writing.

## Steps you can take

1. Read output, not plans, and report what you noticed as a reader. One or two specific observations per round beats a list of ten.
2. Ask the model what general thing caused the problem before asking it to fix the problem. Have the answer written into a rules file.
3. Check the fix on the next piece of output. If the problem recurs, tighten the rule or ask for a check that can run without you. The page on [turning feedback into checks](checks.md) covers that step.
4. Tell the model, in its standing instructions, that you want it to stop and say so when something is wrong, and that a retracted result is better than a quiet one. Then reward that when it happens.
