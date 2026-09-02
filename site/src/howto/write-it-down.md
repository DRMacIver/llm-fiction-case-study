# Write everything down where the model will read it

A Claude Code session has no memory of the previous one. Whatever the model knows about your project when a conversation starts, it knows because a file told it. This constraint shaped the project's structure more than anything else visible in the record, and it is worth internalising early: a rule you gave in conversation binds that conversation only, and a decision you made together but did not record is, for practical purposes, not made.

One thing to be clear about before the list of files. David did not write these files. Nearly every one of them was written, and then maintained, by the model, because David told it to. His contribution was the instruction and the reading afterwards. If the advice below sounds like a lot of clerical work, it is, but it is the model's.

## The files the project ended up with

Every session begins by reading a short root file, `CLAUDE.md`, which is Claude Code's convention for standing instructions. The project's version is a pointer file rather than a rulebook. It lists, in order, what a session must read before writing fiction, and it says why the order matters: exemplar prose first, then the voice rules, then the catalogue of machine-prose habits, then the premise and its hard limits, then canon. Longer documents sit underneath, each with dated rulings at the bottom recording what changed and why. The [rule system page](../workflow/claude-md-rules.md) describes this in more detail.

Three of the underlying files deserve calling out because they solve problems any long project will hit.

The handoff document, `plans/NEXT.md`, exists so a fresh session can recover where the project stands without reading everything. It carries the current state as of a date, a numbered queue of what to do next with enough context to start on item one, and a list of work that is owed but not next. It is edited in place and kept short. Closed items are deleted, not marked done. The [handoff page](../workflow/next-md-handoff.md) has the detail.

The canon files use claim levels. A fact is Established if it is on the page with a citation, Working if it is binding until overruled, or an Open question that must not be resolved casually. This matters because a model will happily state a Working assumption as settled fact, and once it has done that in a few chapters the assumption is settled whether anyone decided it or not. The [canon page](../workflow/canon-and-claim-levels.md) covers it.

The sealed files hold answers to the story's mysteries. They are written by a subagent and kept from David by default, unless he specifically asks to be spoiled, so that he can read the book as a reader would. This exists because of a specific failure: a mystery was introduced on the page, evidence accumulated across chapters, and nobody had decided what the answer was. The fix was not "decide sooner." It was a standing rule that the state of having an undecided mystery on the page is not reachable.

## Why files and not conversation

The obvious reason is memory across sessions. The less obvious reason is that files are where the loop described on [the previous page](the-loop.md) accumulates. Many of the rules in the project's files carry a dated note naming the specific earlier mistake that produced them. That makes the rule system a history of the project's taste as it developed, and it gives a new session the reasons as well as the rules, which should let it apply them to cases the rules did not anticipate.

Files also let rules be checked. A rule written as "avoid decorative endings" is an opinion. A rule written as "chapters end mid-flow on forward-pointing work, with near-zero cleverness in the last two paragraphs" can be reviewed against, and eventually tested for.

## Steps you can take

These are written as advice. Each one describes something David told the model to do rather than something he did by hand.

1. Have the model start a repository, even if you will never write code. Version control is how you get history, and history is how you find out when a rule changed and why.
2. Have the model write a short root instructions file that lists what to read and in what order, and tell it to keep the file under a page and put the long material in separate files it points to.
3. Have the model keep a handoff document from the first day, and make updating it part of the end of every session: the state, the next few things to do, and what is owed, with finished items deleted.
4. When the model states something about your world or your characters, ask whether that is decided or assumed, and have it record the answer with its level. Do not let assumptions harden by repetition.
5. Whenever you give feedback that should apply to future work, end the exchange by telling the model to write it into the relevant file with a dated note explaining why. If you do not, you will be giving the same feedback next week.
