# Royal Road publishing automation

Royal Road, the web fiction site the project's book is published on, has no public API for uploading chapters, only a normal web form. So the project's publishing tool logs in once through a real browser driven by Playwright, then submits the site's own forms directly over HTTP using the saved session, sending what a human filling in the form would send.

## What the tool does

The script, `tools/rr/rr.py`, is invoked with a subcommand for each stage of the process. `login` opens a visible browser window for a one-time manual sign-in, after which the session persists in a git-ignored local profile directory, and `whoami` confirms it is still valid. `create-fiction` posts the initial submission with its cover image and opening chapter. `plan` produces a dry run of a release schedule without touching the live site, so the schedule can be checked before anything actually goes out, and `go` executes that schedule, uploading chapters in order. A separate `regroup` command handles reorganising already-published chapters. It needs several coordinated steps: it deletes drafts that were scheduled but not yet live, removes and re-uploads published chapters, and edits the opening chapter in place, all driven from a JSON file that describes the intended final grouping.

Getting content into the form correctly needed its own conversion step. Chapter markdown uses a small subset of formatting (headings, italics, bold, and boxed "System" text blocks that render the story's game-like status prompts), and `tools/rr_convert.py` turns this into the HTML the form expects. The System boxes needed a workaround. Royal Road's HTML sanitiser strips bare styled divs and spans, so the boxes are built as styled HTML tables instead, since table styling survives the sanitiser where the more obvious markup wouldn't.

## The human boundary

The tool is explicitly designed never to press the equivalent of the site's own "Launch" button, the action that makes a fiction's submission live to readers for the first time. Every command in the tool operates only after that step has already happened by David MacIver's own hand on the actual site. Automation handles the mechanical, repeatable part of getting text formatted and uploaded correctly. The decision to go live is David's alone, and nothing in the tool can trigger it.

Scheduling is handled through Royal Road's own managed-release feature rather than a bespoke queue: chapters are configured with a publish mode, either immediate or scheduled, and a timestamp, recorded in a JSON configuration file alongside the fiction's other metadata (genres, tags, content warnings, the chosen cover image). The project's schedule runs one chapter a day at a fixed UTC time, which is why keeping a buffer of chapters that were already drafted and already checked mattered: falling behind the schedule with nothing ready to fill the next slot is the one failure this whole pipeline is built to avoid.

The session where the drafting pace was checked against the live release schedule, and the decision made to push ahead and build a larger buffer, shows the publishing cadence as a live constraint on drafting decisions rather than an afterthought: [2026-09-02, catching up the publishing buffer](../transcripts/7257e15f-eb7f-4d0b-83e8-dde205ef5352.md).
