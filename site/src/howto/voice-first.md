# Start with the voice, not the story

The first thing David did with the project was not to describe the novel. For the first hour and a half of the very first session, the model did not know what the book was about, and the first two throwaway seed chapters of the actual story came an hour after that. It knew the destination (Royal Road, openly AI-written, good enough to hold up against human genre fiction) and it was set to work on how the narration should sound.

That looks like procrastination and turned out to be the most load-bearing decision in the project. The reason is that a language model's default fiction voice is the single most recognisable thing about it, and it is not fixable after the fact by editing. Every later scene inherits the register the project settles into early, so the register is probably where the effort has the most leverage.

## What actually happened

The [first session](../transcripts/0c653b33-1efd-45bb-b7ab-26ed3dca981e.md) opens with research rather than writing: reading notes on Royal Road's conventions and studying two well-regarded webfiction books, one for the difference between wit that comes from events and wit that is decoration, the other for the observation that good chapters end on a cut rather than a cadence. Then the model drafted three candidate narrator voices with a sample scene for each. None were kept. David pushed for something further from generic web fantasy and a second round produced one called the "Wry Practitioner", which is roughly the voice the published book has now.

Alongside this the model built a document listing what makes prose sound machine-written: particular hedging words, a fondness for arithmetic-flavoured metaphors, a maxim at the end of every paragraph, dialogue in which everyone is equally articulate, endings that land a crafted final beat. That list, tightened repeatedly, is still the backbone of the project's [linting](../workflow/llm-tells-and-linting.md). Its core was written before a word of the actual novel existed, though items like the arithmetic-metaphor tell were added later that day, once eighteen chapters of a first draft had shown the habit.

Only once a voice existed did the premise arrive, and even then the first thing done with it was to write two chapters as exemplars to be imitated, not as chapters to be kept. Everything before the premise is shown unredacted in the transcript, sample scenes included, because none of it concerns the eventual book.

## Steps you can take

1. Before describing your story, spend a session on register. Give the model examples of prose you admire and, more usefully, examples you dislike and can say why. Ask for three or four different narrator voices as short sample scenes on a throwaway subject.
2. Read the samples as a hostile reader and say precisely what sounds generated. Be concrete: not "too polished" but "every paragraph ends with a little summarising judgement" or "every character answers the exact question they were asked." Tell the model to keep a file of those observations and to add to it as you go. David never wrote that file himself. He named the problem and the model wrote the entry.
3. Pick a voice and have the model write one or two short pieces in it that you actually like. These are your exemplars. Keep them somewhere safe and never delete them. The project did delete its first exemplars as scaffolding and spent some hours the same afternoon diagnosing the voice drift that caused before restoring them. See [the chronicle for 24 August](../chronicle/2026-08-24.md).
4. Only now introduce the story. The rules about voice should already be written down by the model and the exemplars should be the first thing a drafting session reads, before the rules. The project's [voice memo](../workflow/voice-and-exemplars.md) makes this order explicit and says that where a rule and an exemplar disagree, the exemplar wins.

## Why exemplars beat rules

The project learned this the hard way. An early attempt to draft from the written voice rules alone, without the exemplar prose in context, produced text that satisfied every rule and still read as generic. A rule like "no more than one narrator aphorism per scene" tells a model what to avoid without telling it what the voice sounds like when it is working. Rules are good at annotating examples, pointing at what to notice, and poor at substituting for them. If you take one practical thing from this page, it is that your project needs a small set of pieces you are happy with, read first, every time.
