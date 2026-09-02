# Write everything down where the model will read it

A Claude Code session has no memory of the previous one. Whatever the model knows about your project when a conversation starts, it knows because a file told it. This is the constraint that shaped the project's whole structure more than any other, and it is worth internalising early: a rule you gave in conversation binds that conversation only, and a decision you made together but did not record has not, for practical purposes, been made.

## The files the project ended up with

Every session begins by reading a short root file, `CLAUDE.md`, which is Claude Code's convention for standing instructions. The project's version is a pointer file rather than a rulebook. It lists, in order, what a session must read before writing fiction, and it says why the order matters: exemplar prose first, then the voice rules, then the catalogue of machine-prose habits, then the premise and its hard limits, then canon. Longer documents sit underneath, each with dated rulings at the bottom recording what changed and why. The [rule system page](../workflow/claude-md-rules.md) describes this in more detail.

Three of the underlying files deserve calling out because they solve problems any long project will hit.

The handoff document, `plans/NEXT.md`, exists so a fresh session can recover where the project stands without reading everything. It carries the current state as of a date, a numbered queue of what to do next with enough context to start on item one, and a list of work that is owed but not next. It is edited in place and kept short. Closed items are deleted, not marked done. The [handoff page](../workflow/next-md-handoff.md) has the detail.

The canon files use claim levels. A fact is Established if it is on the page with a citation, Working if it is binding until overruled, or an Open question that must not be resolved casually. This matters because a model will happily state a Working assumption as settled fact, and once it has done that in three chapters the assumption is settled whether anyone decided it or not. The [canon page](../workflow/canon-and-claim-levels.md) covers it.

The sealed files hold answers to the story's mysteries. They are written by a subagent and never shown to David, so that he reads the book as a reader would. This exists because of a specific failure: a mystery was introduced on the page, evidence accumulated across chapters, and nobody had decided what the answer was. The fix was not "decide sooner." It was a standing rule that the state of having an undecided mystery on the page is not reachable.

## Why files and not conversation

The obvious reason is memory across sessions. The less obvious reason is that files are where the loop described on [the previous page](the-loop.md) accumulates. Almost every rule in the project's files exists because of a specific earlier mistake, and the file records both the rule and the mistake. That makes the rule system a history of the project's taste as it developed, and it means a new session inherits not just the rules but the reasons, which lets it apply them to cases the rules did not anticipate.

Files also let rules be checked. A rule written as "avoid decorative endings" is an opinion. A rule written as "chapters end mid-flow on forward-pointing work, with near-zero cleverness in the last two paragraphs" can be reviewed against, and eventually tested for.

## Steps you can take

1. Start a repository, even if you will never write code. Version control is how you get history, and history is how you find out when a rule changed and why.
2. Write a short root instructions file that lists what to read and in what order. Keep it under a page. Put the long material in separate files it points to.
3. Keep a handoff document from the first day. Update it at the end of every session with the state, the next few things to do, and what is owed. Delete finished items.
4. When the model states something about your world or your characters, ask whether that is decided or assumed, and record the answer with its level. Do not let assumptions harden by repetition.
5. Whenever you give feedback that should apply to future work, end the exchange by asking the model to write it into the relevant file with a dated note explaining why. If you do not, you will be giving the same feedback next week.
