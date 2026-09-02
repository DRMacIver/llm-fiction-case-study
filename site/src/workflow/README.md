# The workflow

This section describes the tooling and the process behind "How to Save the World", separately from the day-by-day chronicle of what actually happened while it was in use. The chronicle tells the story of the ten days and this section explains the machinery running underneath them. The two overlap a good deal, and each links to the other where that helps.

## The shape of a chapter's journey

A chapter starts as a line in a plan: a book overview breaks into arcs of 30,000 to 50,000 words, and an arc breaks into scenes of 600 to 900 words, which is the actual unit of drafting. A scene breakdown has to pass a mechanical check before any prose gets written: no scene's "discovery move" (the thing that changes for the reader) may repeat within four consecutive scenes. This rejection gate exists because it failed once, mid-project: one discovery move ran ten times across Arc 3, four of them inside a single four-scene window, dragging a six-chapter stretch, and the repair cost a chapter rebuild and two full revision passes. Catching it before drafting is much cheaper than catching it after.

Scenes get drafted, then run through several passes: a canon-consistency check against the established facts of the story so far, a farming-facts check (the world's magic only modifies real agricultural problems, so every claim needs a real basis), an editing pass split into a sense check and a voice-compliance check, and a language-police pass hunting the reflexive habits that mark prose as machine-generated. Scenes that clear all of this get grouped into roughly 2,000-word chapters, and the chapters that clear a further author's read go into the publishing schedule.

## Human and model

David MacIver set the premise, wrote the rules the model works under, read finished chapters, and made every judgement call the tooling flagged as needing one. The model did the drafting, the checking, and, in several cases, the design and implementation of the checking tools themselves. The notes that appear at the top of a Royal Road chapter, the ones addressed to readers as the author, are the one piece of text the rules forbid the model from drafting at all. Everything else, story prose and the in-story notes at the foot of each chapter included, is machine-written, and the book says so on its own page.

The working relationship was adversarial in a useful sense: David's role was largely to catch places where the model's own quality bar had slipped, and a fair amount of the tooling described here exists because a first version of some check missed something and got tightened afterwards.

## Sessions, subagents, and workflows

Claude Code sessions run at three different scales in this project. A single interactive session, with David typing prompts and reading replies, did most of the actual drafting. The project's notes are explicit that this was deliberately not delegated to subagents, because a persistent session holding the whole conversation in mind produced better prose than a first attempt that split drafting across independent agents.

Checking work is different. A canon check, a farming check, or a pre-emptive editorial read runs well as a subagent, because it's a bounded task with a clear brief and no need for the accumulated context of a drafting session. Several of the multi-stage checks, the language-police pass in particular, run as a fan-out of several small model calls followed by one larger model reconciling their findings, which is cheaper and, on this project's own tests, more reliable than one large model doing the whole pass alone.

Workflows sit above both: a scripted sequence that runs a whole pipeline stage without a human watching each step, such as running a consistency check across every accepted chapter at once. These are used for large, mechanical sweeps where the individual judgements are well-specified enough that they don't need David reading each one as it happens, only the summary at the end.

## What follows

The rest of this section takes the pieces one at a time, roughly in the order a chapter meets them: the rule files a session reads before it writes anything, the exemplar-first method for holding a voice, the tooling that hunts machine-prose habits, the canon system, the handoff document, and then the parts of the pipeline that happen after the prose is accepted, which is proofreading on an e-reader, commenting, publishing, and the sweeps that check a finished book against itself. Most of these pages end with the failure that caused the rule, because in this project that is usually the real explanation.
