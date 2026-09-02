# Delegate by kind of work, not by volume

Claude Code offers work at three scales: the main conversation, subagents, and workflows. In the main conversation, you type and the model replies and everything said so far is in view. Subagents are separate conversations the main one spawns to do a bounded job and report back. Workflows are scripted sequences that fan many subagents out over a list of items and collect the results without anyone watching each step. The project used all three and, after some false starts, settled on a fairly clear division.

## What stayed in the main session

Drafting. The project's notes are explicit that prose was written in the main interactive session on purpose, because a persistent conversation that holds the voice, the recent scenes, the exemplars and David's last few notes in mind produced better prose than a fresh subagent working from a brief. An early experiment that split drafting across independent character-voice subagents produced strong individual lines that collided on shared rhetorical devices, and it was not repeated.

Judgement calls also stayed in the main session. That covered anything where the answer depended on taste, or on a decision David hadn't made yet. The rest of the division was shaped by cost. On 25 August David told the model to do most work in subagents and workflows and to keep the most expensive model for the main session only. On [27 August](../chronicle/2026-08-27.md), after a workflow used up the week's allowance for that top model, he wrote the rule down: never run subagents on the top-tier model, use the next tier for judgement-heavy work, and a cheaper one for mechanical passes.

## What went to subagents

Bounded checks with a clear brief. A canon-consistency check on one scene, a farming-facts check, a pre-emptive editorial read against a named list of criteria. These do not need the accumulated context of the drafting conversation, they benefit from a fresh reader who has not been staring at the scene for an hour, and they can run in parallel while the main session moves on.

Sealed work. Subagents write and edit the answers to the story's mysteries, so they never enter the main conversation and never reach David unless he asks to be spoiled, because he wanted to read the book as a reader. This is delegation as an information barrier rather than as a labour saving, and it is a use of subagents that does not seem widely known.

## What went to workflows

Sweeps. When the same check has to run over every chapter in a book, or several hundred small review calls have to hunt for prose habits across a whole manuscript, a scripted workflow runs them and produces one report. The [language-police pass](../workflow/llm-tells-and-linting.md) on 31 August ran several hundred review agents in total. The [consistency workflow](../workflow/consistency-workflows.md) runs one cheap agent per chapter and then a synthesis step. In each case the parallel part is narrow and cheap and the serial part is where the judgement sits.

The project also used an unattended mode for long stretches of settled work. Twice David handed the model a brief, a set of default decisions to make in his absence, and a stopping rule, and left it to run. The [first](../chronicle/2026-08-25.md) produced the first complete draft of book one overnight. The [last](../chronicle/2026-09-02.md) drafted the rest of the book in under three hours with instructions to stop if quality visibly slipped. This depended on what the [previous pages](write-it-down.md) describe: the rules were in files, the checks ran without him, and a handoff document told the model what to do when it hit a decision.

## How supervision changed over time

The clearest illustration is the redraft of the second act on [31 August](../chronicle/2026-08-31.md). It started with a deliberately gated pipeline: draft one scene, run four checks (the self-check, the canon check, the craft review and the overlap check), commit, show David, wait. As scenes came back clean he loosened the gate, approving in batches, and by the end of the day he asked for the rest of the act to be drafted straight through. He earned the trust per scene and reduced the supervision in steps, not all at once. Two days later the same pipeline ran unattended to the end of the book.

## Steps you can take

1. Draft in one long conversation with the exemplars and rules loaded. Do not split creative work across agents to go faster. You will get speed and lose coherence.
2. Hand bounded checks to subagents with a written brief and a fixed list of things to report. Run several at once.
3. When something has to run across everything, script it, with a cheap model per item and a careful model reconciling the results.
4. Start supervised and loosen deliberately. Approve one unit, then batches, then stretches. Have the model write down a stopping rule before you leave it alone. The rules and handoff notes it maintains should be good enough that a stranger could pick up the work from them, since that is effectively what is happening.
