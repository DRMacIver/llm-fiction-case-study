# How this site was built

The site was built by one Claude Code session over roughly a working day, with almost all of the labour done by subagents launched from it. The session's own job was to decide what to do next, write the prompts, read the reports and commit. It also wrote the how-to section and this one directly, after David asked for synthesis rather than more delegated summary.

## The pipeline

Everything on the transcript pages comes from a four-stage Python pipeline that reads the novel project's session files where Claude Code keeps them and never copies them into the repository.

The parser reads each session's JSONL file and its subagent and workflow directories, and produces one JSON document per conversation. It reassembles the model's interleaved thinking, text and tool calls into turns, links each Agent call to the child transcript it spawned, and reduces every tool call to a single line: a file path for reads and edits, a truncated command for shell calls, a description and model for agents. File contents are dropped at this stage, so nothing downstream can leak them. The one exception, added later at David's request, is the first eighty minutes of the first session, before the story premise had been given, whose sample scenes and notes are shown in full.

The prose index builds a set of hashed seven-word shingles from every unpublished story file, including drafts that were deleted and exist only in git history. It stores hashes rather than text.

The redactor applies, in order: private-information patterns (local paths, session identifiers, addresses), a curated list of spoiler terms and their variants, sentence-level patterns for the hard spoilers, an "unpublished" tag on any scene number above the published boundary, and finally the shingle check, which blanks any sentence sharing a seven-word run with unpublished prose. Markers are deliberately uninformative. An early version labelled each one with the category or topic it had removed, and David pointed out that "redacted sentence: plague" is not much of a redaction.

The renderer turns the redacted JSON into mdBook pages for the nine sessions and standalone HTML pages for the 1,712 subagents, which are kept out of the sidebar because a sidebar with 1,700 entries is not a sidebar. Conversation text is rendered from Markdown to HTML with raw HTML escaped and only explicit URLs linked.

## The workflows

Six Workflow runs did the bulk of the work. Each is a script that fans agents out over a list and collects their structured output.

**Foundations** scaffolded the repository and the mdBook site, wrote the parser, and sent eight Haiku agents through the novel's notes, plans and unpublished scenes to list every spoiler term, with three more building an allow-list of names that had appeared in the published scenes. A Sonnet agent merged the lists into the redaction config and wrote the redactor and renderer. Fourteen agents.

**Content** fixed the sidebar problem, swept every rendered page for leaks with Sonnet on the main sessions and Haiku on the subagents, summarised each session, had Haiku summarise each day of the novel's git history and research each area of its tooling, and then had Sonnet write the chronicle and the workflow pages from those summaries. An Opus editor wrote the introduction and the disclosure page and edited everything for voice and consistency. Eighty-three agents.

**Prose guard** added the shingle index after the leak sweep found quoted draft prose that no term list could catch, then swept the main sessions again. Twenty-two agents.

**Render review** came after David looked at the live site and found unrendered Markdown, harness notifications attributed to him, and other basic errors. Ten Sonnet reviewers sampled pages and catalogued 29 defect classes. One fixer traced them to a handful of root causes and added 38 regression tests. A pre-premise agent in that run was blocked by a safety classifier and had to be rerun on its own. Seventeen agents.

**Writing check** fact-checked the prose pages. It is described in [What went wrong](what-went-wrong.md), because of what it found. One hundred and thirty agents.

**Voice pass** ported the voice-checking method from «OTHER-PROJECT»: a mechanical linter and a catalogue of named devices, three blind reviews per page, one editor per page with every fact frozen, and a diff check per page for any claim that had moved. One hundred and seventy-two agents.

Between the workflows, a dozen or so single agents did bounded jobs: convert Markdown in the transcripts to HTML, implement the pre-premise rule, research the two source projects' checking practices, gather current Claude Code setup facts from the documentation, apply the fact-check fixes, and render this project's own transcripts for this section.

## The division of labour

David's instructions put the expensive model at the top and cheap ones at the bottom, and the split held. Haiku did the reading that needed coverage rather than judgement: spoiler-term extraction, git-log summaries, tooling research, claim extraction, subagent leak sweeps. Sonnet did everything that needed to produce a correct artefact: scripts, tests, drafts, verification with receipts, edits. Opus did two editing passes and one synthesis. The session itself wrote prompts, the how-to section, this section, and a handful of small edits, and read every report.

The pattern that recurs in the novel project, cheap and narrow first and then careful and broad, recurs here too, and for the same reason. Where it was not followed, the results were worse. The first rendering pass was one Sonnet agent asked to fix one thing, and it introduced two new classes of bug while fixing it.
