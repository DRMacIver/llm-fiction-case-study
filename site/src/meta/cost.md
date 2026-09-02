# What it cost

David asked for a stop if the work passed half of his remaining weekly allowance. At the start he was at 16 percent of a 20x Max plan with a temporary 50 percent boost, and the session's working estimate was that it could spend roughly the equivalent of nine hundred dollars of API usage before stopping. It did not get close, though the figures below are for the site only and come on top of the novel, which had already used most of that week.

## Agent tokens by workflow

| Workflow | Agents | Tokens |
|---|---|---|
| Foundations | 14 | 1.1M |
| Content and edit | 83 | 6.1M |
| Prose guard and re-sweep | 22 | 1.5M |
| Render review and fixes | 17 | 1.6M |
| Writing check | 130 | 6.6M |
| Voice pass | 172 | 8.4M |
| Single agents, six | | 0.7M |
| Total | about 450 | about 26M |

Tokens here are as reported by the Workflow tool for its subagents, mostly input, spread across Haiku, Sonnet and Opus. The session's own context is not included. The two checking passes, fact and voice, are more than half the total, which matches David's observation about the novel: the cost was dominated by checking rather than by drafting.

## What the money bought

The first two workflows, about a quarter of the spend, produced a complete site: pipeline, redaction, rendered transcripts, workflow pages, chronicle, introduction. Everything after that was correction. About a fifth went on fixing rendering and redaction defects that reading the output would have caught earlier and more cheaply. More than half went on checking the prose, first for truth and then for voice, and the truth check found 22 errors in pages that had already been through an Opus editing pass.

A cheaper run of the same project is easy to describe with hindsight. Look at the rendered output before committing it. Write the link checker before the first deploy. Run the fact-check before the voice pass rather than after the pages have been live for hours. None of that needed a larger model. It needed the session to spend more of its own attention on the artefact and less on the reports.

## Time

The session ran through most of one day. The longest single wait was the render review at nearly forty minutes of wall-clock time, most of it one fixer working through 29 defect classes in sequence. The voice pass ran 172 agents in about eighteen minutes because almost all of them ran in parallel. The two things that took longest in practice were not workflows at all: David reading the live site and coming back with what was wrong, and the session then working out which layer of the pipeline had caused it.
