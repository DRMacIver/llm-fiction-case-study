# The making of the making of

The rest of this site describes how a novel was written with Claude Code. This section describes how the site was written with Claude Code, in one long session on 2 September 2026, two days after the novel's first chapters went live. It is here because the same questions apply. The site is a piece of writing produced by a model under a human's direction, it needed rules, checks and several rounds of correction, and some of what went wrong is more instructive than what went right.

It is written in the first person, unlike the rest of the site, because the thing being described is the session that is writing it. That is also why the section can never be quite complete. The transcript of this session, linked from the [transcripts page](transcripts/index.md), ends before this page was finished, and any later edits to it happened in sessions the transcript does not show.

## What David asked for

The brief arrived in one message. Build a website chronicling the novel's construction, because people had been asking about the workflow. Draw on the notes about David's writing voice kept in a separate project of his, anonymised throughout this section as «OTHER-PROJECT», while making clear the site is fully automated. Render the Claude Code transcripts of the novel project with spoilers redacted, file contents hidden and tool use simplified, doing as much of that as possible by script before any model saw the text. Describe the workflow's features and write a chronicle. Use mdBook, plain rather than decorative. Do the work through the Workflow tool, with Haiku for grunt research, Sonnet for routine work and Opus coordinating, and keep the top-tier model's own effort to a minimum. Stop if the spend passed half of David's remaining weekly budget. Then, after a few questions, leave it to run.

The questions settled the published boundary (scenes 1 to 40, from the novel's publishing map), where the transcripts would be read from (in place, never committed raw), how aggressive redaction should be (aggressive by default, with judgement calls where a transcript became unreadable), and the site generator. David added the repository name and asked for GitHub Pages later, mid-run.

## The pages

[How this site was built](how-it-was-built.md) walks through the pipeline and the six workflows that produced the site, in order.

[What went wrong](what-went-wrong.md) is the list of failures: rendering bugs that survived to the live site, a redaction that leaked the reason for redacting, harness messages attributed to David, and the fact-check that found the model had made things up about the project it was documenting.

[What it cost](cost.md) gives the token figures and what they bought.

[Transcripts of this project](transcripts/index.md) are the sessions themselves, redacted more lightly than the novel's: private information is removed, the separate project is anonymised, and the handful of hard spoilers the prompts had to name are blanked, but nothing else.
