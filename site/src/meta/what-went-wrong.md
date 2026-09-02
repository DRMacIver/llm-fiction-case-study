# What went wrong

This is the more useful page. Each item is something that reached the committed site, or David, before it was caught, apart from the first, which was caught from an agent's report just before it would have. Each one has a lesson attached that the how-to section states more politely.

## The sidebar with 1,712 entries

The first renderer put every subagent transcript into mdBook's table of contents, because mdBook only builds pages that appear there. The result was a 133 megabyte site with an unusable sidebar. The fix was to render subagent pages as standalone HTML that mdBook copies through unchanged, and link to them from the parent session. The agent that wrote the first version had followed the tool's rules correctly and produced something nobody could use. Nobody had looked at the output before it was committed.

## Markdown that did not render

The fix for the sidebar wrapped conversation text in raw HTML blocks so the pages could carry labels and borders. mdBook does not process Markdown inside raw HTML, so every list, heading and bold span in every transcript showed as literal asterisks and hashes on the live site. David saw it first. The fix was to render the Markdown to HTML in Python before embedding it, with raw HTML in the source escaped rather than passed through. It then turned out that mdBook ends a raw HTML block at the first blank line, which had been silently breaking three transcripts in a way nobody had noticed either.

## Redaction that said what it was hiding

Every redaction marker carried its category or topic: "redacted: character", "redacted sentence: plague/epidemic". This was in the spec the session wrote, was implemented faithfully, and was pointed out by David as a spoiler in itself. Markers are now a bare "redacted" or "redacted sentence", with only "private" and "unpublished prose" labelled. The lesson is not about redaction. It is that the person who writes a specification is a poor judge of whether it makes sense, and this session wrote that one.

## Harness messages attributed to David

Claude Code delivers background notifications, task completions, and command output in the user role. The parser treated everything in the user role as something David typed, so the transcripts showed him apparently saying "task-notification" and pasting system reminders. Some of those notifications also carried identifiers that the private-info redactor then blanked, producing a David who appeared to be talking in redaction markers. Ten reviewers sampling pages found this and 28 other defect classes in one pass. Most traced back to a few root causes in the parser.

## Over-eager URL detection

Turning bare URLs into links, at David's request, also turned filenames such as notes.md into links to http://notes.md, and caught a regex fragment in one transcript. Linkification now applies only to explicit http and www addresses, and any anchor that does not point at one is unwrapped.

## Section pages that did not exist

Every link to a section overview pointed at README.html, which mdBook never produces because it renders README.md as index.html. Nested subagent links doubled a directory name. A link checker over the built site found 56 broken links in three classes. The checker was written after David reported broken links, not before the first deploy.

## The fact-check

This one is the reason the section exists. After the how-to pages were written, David asked for a fact-checking skill built from the practices in the two source projects, and for it to be run over the site. It extracted 484 claims from 34 pages, verified each blind against the transcripts and git history, cross-checked six topics across pages, and sent every negative finding to a second agent whose job was to refute it. Twenty-two problems survived. Two findings were refuted.

Most of the problems were in the pages this session had written directly, and they were the kind that makes a story tidier than the record. "A day and a half" of voice work before the premise was in fact eighty minutes. "Two scenes redrafted that night" was one. An overlap checker "built the day before" a discard was built four minutes before it. The clearest worked example on the loop page attributed the wrong complaint to the wrong session. One sentence cited "the project's own notes" for a characterisation that appears in none of them. In the delegated pages, Royal Road publishing was described as browser automation when it is HTTP after a browser login, and the order of a repository cleanup and a redraft was reversed.

Then, on David's reading, the check had missed something no claim-level check could see. The how-to pages kept telling the reader to "keep a file" or "write a rule", when the record shows David doing almost none of that himself. He told the model to write and maintain the files. The advice had drifted from what happened to what sounded like advice. That was rewritten by hand, and it is worth saying that the fact-check, which found 22 real errors, did not find the largest one.

## The voice pass that moved facts

The last pass edited every page for voice under an explicit rule that no fact, number, date, name or link could change. A diff check on each page afterwards found that editors on 22 of the 34 pages had changed one anyway: a softened quantity word, a dropped qualifier, a new justification, a claim that everything was covered below. All were reverted. The editors were Sonnet agents given clear instructions and a frozen-facts rule in bold, and it did not hold. The check that caught them was a separate agent with only the diff and no knowledge of why the edit was made.

## What this adds up to

All but one of these were caught by David or by a check that ran after David complained, the exception being the fact-check errors, which were caught by a check David asked for. None was caught by the session reading its own output, because the session mostly did not read its own output. Even the sidebar was caught from a size figure in a report. It read reports about the output, written by the agents that produced it. That is the same failure the novel project spent ten days building tooling against, and this section is evidence that knowing about it is not the same as avoiding it.
