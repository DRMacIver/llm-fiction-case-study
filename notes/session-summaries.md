# Session summaries

Spoiler-free narrative summaries of each Claude Code session behind the "How to Save the World" project, built from chunk-level sweep summaries. Dates are UTC.

## 0c653b33-1efd-45bb-b7ab-26ed3dca981e — Finding the voice and starting the draft
**2026-08-24 to 2026-08-25**

The opening session of the project. It began with research into Royal Road conventions and several rounds of testing narrator voices, drawing craft lessons from published web fiction about the difference between meaningful, event-driven wit and mere ornamental wit, and about how strong endings cut rather than resolve neatly. Once a voice was settled, the real story concept arrived and the collaborators built out canon files, two editing skills, core worldbuilding, thematic direction, and a cast, then moved into planning chapter arcs with open questions tracked for later.

The second half of the session establishes a formal decision-making regime for locking in choices at the right moment, locks the ending direction, plans a five-book series, and diagnoses a voice-drift problem in the drafting pipeline, fixed by restoring exemplar chapters and gating drafts on a voice check. A blind test comparing two models for drafting settled on a policy of one model drafting and another judging and editing. The session ends with the author handing off unattended work to finish book one, including a set of default decisions to make in their absence, aimed at producing a finished epub.

## 10c1dd77-c31a-4be9-a7b6-23651a4792b4 — Building the System and starting the draft
**2026-08-27**

This session built the setting's magic system, aging and calendar rules, and worked through extensive geography, history, and institutional worldbuilding, alongside a theme file anchored on the idea that the world always needs saving. Tone was deliberately calibrated away from cosy fantasy toward competence-driven storytelling. A claim-graded canon structure (established, working, and open ideas) was set up to track what was locked in versus still under discussion.

After this the book was restructured into a formal book, arc, and chapter authorship system, throwaway seed material was deleted, and the collaborators planned book one into three arcs before beginning to draft the first. The session pauses mid-draft so the author could rule on a set of open story decisions before the agent resumed.

## 3ef92e14-71be-4557-a7d1-f251a7410081 — Rebuilding the draft through several full rewrites
**2026-08-27 to 2026-08-30**

A long session spanning several distinct phases of work. It opens with the earliest voice iteration (moving through several drafts before settling on a mature style) and a multi-agent experiment where isolated character-voice subagents wrote strong individual lines but collided on shared rhetorical devices, which led to methodological findings that the scoring instruments being used to compare drafting approaches were unreliable and some earlier claimed results had to be retracted. An autonomous overnight run then sealed outstanding canon mysteries, resolved a large backlog of open worldbuilding questions, and built a citation checker that caught canon files misquoting draft chapters.

The session then moves into a full scene-granular replanning and rewrite of book one's opening arc, gated on quantitative craft criteria, followed by detailed editorial rounds on early scenes catching contradictions, flat prose, and voice violations, plus fixes to the review tooling itself. A deep worldbuilding thread works out how magic functions underneath the System. The session ends in the middle of a rewrite of book one's second act, after the collaborators discovered that newly drafted scenes had leaked substantial verbatim text from earlier, discarded drafts; the affected material was quarantined and new rules were written to prevent it happening again, with a handoff prepared for a fresh session to redraft carefully, scene by scene.

## 61a194e2-4e55-494c-bb3e-5d225e267758 — Working out the world's material history
**2026-08-25 to 2026-08-27**

A short worldbuilding session. The author asked for a historical development timeline covering the period from the setting's magical tradition beginning up to the story's present day, to avoid the setting feeling anachronistically modern; this covered the development of agriculture, paper, and other everyday materials. The session then worked out limits on how far magic can improve farming practice, worked out population and mage density figures for the setting, and designed a separate, more restricted and church-controlled tradition of healing magic that deliberately contrasts with the diffuse, folk-driven farming tradition at the story's centre.

## 7257e15f-eb7f-4d0b-83e8-dde205ef5352 — Drafting to the end of book one
**2026-09-02**

The bulk of this session is a late push to finish drafting book one. The author asked the agent to draft the remaining scenes with periodic independent quality checks, stopping if quality degraded. The agent worked scene by scene through a pipeline of drafting, canon review, voice review, and an overlap check against earlier discarded material, redrafting some scenes from scratch and extending the book into its final act, finishing the draft and updating the project's status notes.

Earlier in the same file is an unrelated piece of tooling work: writing a script to sync the book's epub to a Kindle, diagnosing a page-turning freeze caused by a stale sidecar file and an outdated ebook format, and building a tool that remaps a reader's position across later text edits.

## 92c486ed-62f3-40a9-8d7d-b9dd6554d07e — Syncing the book to a Kindle
**2026-08-25**

A short tooling session. The author asked for a script to sync the latest epub build to a mounted Kindle. The agent built it, diagnosed a page-turning freeze caused by a stale index sidecar file and an outdated ebook format, switched to a modern format with freshly regenerated pagination data, and then built and tested a module that keeps a reader's position stable across later text edits by anchoring to the surrounding prose, validating it against a real historical edit and an end-to-end device test.

## be6bcf16-d9e6-4525-85d6-ce35993a5324 — Building a local commenting tool
**2026-08-25**

A short session building a local web-based reading and commenting tool, styled after Royal Road's reading interface, with text-selection commenting and logic to keep comment anchors attached to the right text as chapters are edited. Two small follow-up requests made scene-break dividers more visible and styled in-story system message boxes to match Royal Road's presentation.

## c214c046-1bb3-4385-abee-f924d8349bad — Redrafting the second act, scene by scene
**2026-08-31**

A short session continuing the redraft of book one's second act, using a gated pipeline of drafting, automated review, and author approval scene by scene. Partway through, the agent recognised a risk that its context for a new scene included too much of an earlier, discarded draft, and paused to flag the issue before continuing rather than risk repeating the contamination problem from earlier in the project. The author reviewed and approved the work with minor comments.

## d1679987-c781-4167-82f2-4fb2b67962c1 — Finishing the rewrite and publishing to Royal Road
**2026-08-30 to 2026-08-31**

This session finishes the scene-by-scene redraft of book one's second act, with the review process gradually loosening from single-scene gates to drafting straight through as trust built. It then pivots to publishing: the collaborators settled on the series title and blurb, built a tool to convert chapters to Royal Road's formatting and submit them directly, and cleaned up the working repository while preserving history.

The rest of the session covers preparing the book for a public audience: writing in-story author's notes in a consistent fictional persona, fact-checked against real-world farming knowledge, and building an automated linting pipeline that combines rule-based checks with model-based review to catch recurring machine-writing tells across the manuscript. The book was submitted to Royal Road, the first chapters were published, and remaining chapters were scheduled for daily release; a late realisation that chapters were shorter than typical for the platform led to the scenes being regrouped into fewer, longer chapters before republishing.
