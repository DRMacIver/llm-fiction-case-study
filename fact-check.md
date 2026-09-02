## Resolution (2026-09-02)

Fixes applied for the numbered problems below, all in `site/src/workflow/*.md`, `site/src/chronicle/*.md`, `site/src/about.md`, and `site/src/transcripts/titles.json`. Items in `howto/` are the other editor's and are marked as fixed separately.

1. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
2. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
3. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
4. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
5. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
6. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
7. `workflow/README.md`: replaced the invented "a dozen times across fifty-odd scenes, six of them inside a seven-scene stretch" with the sourced figures, "ten times across Arc 3, four of them inside a single four-scene window, dragging a six-chapter stretch".
8. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
9. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
10. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
11. `workflow/overlap-checking.md`: reattributed the never-open rule from `CLAUDE.md` to the project's voice document, written as prose rather than a code-style citation.
12. `workflow/royal-road-publishing.md`: rewrote the opening claim so the tool is described as logging in once through Playwright and then submitting the site's own forms directly over HTTP, rather than driving the whole publishing flow through a browser.
13. `workflow/next-md-handoff.md`: replaced the "advisory pass checking that explanations weren't cut for brevity" description with the actual mechanical "because"/write-verb-tic thinning pass.
14. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
15. `workflow/canon-and-claim-levels.md`: changed the canon-conflict resolution from "both get flagged, and the decision belongs to David" to "canon wins and the earlier chapter is flagged for revision", matching the consistency-check skill.
16. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
17. `workflow/farming-facts-and-author-notes.md`: changed the transcript link text from "2026-08-31, redrafting scene by scene" to "2026-08-31, mapping the setting". `site/src/transcripts/titles.json`: checked both sessions' first user turns in `build/parsed/index.json` and corrected the mislabelling; `c214c046` (an 08-31 session whose first turn asks for an SVG map of the setting) now carries a title and blurb describing the mapping session, and `d1679987` (the 08-30/08-31 session whose first turn is the scene-by-scene redraft brief) keeps the "Finishing the rewrite and publishing to Royal Road" title and blurb, which already matched its real content.
18. `workflow/overlap-checking.md`: corrected the sequence so the repository cleanup that deleted the discarded drafts is described as happening on the morning of 31 August so the overlap checker could run against git history during that day's redraft, rather than after the redraft was accepted.
19. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.
20. `chronicle/2026-08-25.md`: changed the language census range from "chapters 1 to 21" to "chapters 1 to 23", matching the source note and `workflow/llm-tells-and-linting.md`.
21. `about.md`: scoped the File contents paragraph to note the pre-premise exception in the project's first session, with a pointer to `howto/voice-first.md`.
22. howto pages: fixed by the session editor, together with a reframing so every 'Steps you can take' item says the model writes and maintains the file on the author's instruction, and softening of the unverifiable claims listed below.

Drift and ambiguity fixes also applied, on their own clear evidence:

- `workflow/README.md`: dropped the unsupported "unless it's one continuous action split across them" exception to the four-scene repeat rule; no source uses this framing.
- `workflow/canon-and-claim-levels.md`: changed "core facts and continuity first, softer thematic consistency last" to "core facts and continuity first, with theme weighted softer than the rest", since theme is not literally last in the consistency-check skill's priority list.
- `workflow/next-md-handoff.md`: reworded "canon files, which do keep dated history at the bottom" to describe dated rulings as a permanent record woven through the file, since they are interleaved through `notes/canon/characters/*.md` rather than gathered at the foot.
- `chronicle/README.md`: changed "dozens of them" to "over a hundred of them" for the fabricated citations, matching the precise count (110) given elsewhere on the site.

Drift and ambiguity items reviewed and left alone because they need author judgement rather than a clear-cut correction:

- `workflow/voice-and-exemplars.md` lines 11 and 17: flagged as paraphrases presented close to quotation ("Rules exist to annotate the exemplars"; the "don't listen perfectly" rationale). Both are fair summaries of source material rather than errors, and the fact-check proposes no specific rewording, so left as the author's own phrasing.
- `chronicle/2026-08-26.md` ("already been established"): checked against the source: the page already separates the pre-existing green-revolution framing ("had already been established") from the specific ceiling rule settled that day ("the limit settled on was"), which is the distinction the fact-check asked for. No change needed.

# Fact check of the site prose

Date of check: 2026-09-02.

Pages checked: `site/src/introduction.md`, `site/src/about.md`, `site/src/howto/*.md`, `site/src/workflow/*.md`, `site/src/chronicle/*.md`.

Sources used, in priority order: the parsed transcripts under `build/parsed` (main sessions and subagents) and the git history of the novel repository; `build/parsed/index.json` and `site/src/transcripts/titles.json`; `notes/session-summaries.md`; the Claude Code documentation at https://code.claude.com/docs/en/ for `howto/setup.md`; and the site pages themselves for internal cross-references.

Revisions at the time of the check:

- site repository (`autoroad-howto`): `749d075c14ea2562eb4e26d7e23cff7418c06ed2`
- novel repository (`autoroad`): `47781bfbc97ece7979f27c6e354cf064bb37e888`

Mechanical pre-pass (`build/writing-check/prepass.md`, generated by `tools/check_prose.py`, 7 pytest tests passing): 83 of 83 internal links resolve, 47 of 47 dates fall inside the project window, 175 topical numbers plus 156 informational numbers extracted for checking, 0 hits on banned content patterns.

Counts: 22 problems found (17 claim-level, 5 cross-page contradictions), 29 unverifiable or unchecked claims, 26 drift and ambiguity notes, 2 findings rejected on refutation.

## Problems found

Listed most consequential first. Each entry gives the claim, the receipt, the reasoning, and the fix proposed. No site page was edited.

### 1. `howto/README.md` line 15: "covers the first day and a half, in which no fiction was written"

Wrong. I ran `git -C /Users/drmaciver/Projects/autoroad log` myself: commit `b6cd810`, 2026-08-24 14:16:45 +0100, "Add concept notes and two seed chapters", adds `chapters/001-the-wrong-man.md` (301 lines) and `chapters/002-the-call-declined.md` (220 lines) of actual prose fiction, roughly two and a half hours into the project's first session. Further chapter drafts follow the same day (`504b550`, `731c3e3`, `70e763e`). The site's own `howto/voice-first.md` agrees against this page: "the first thing done with it was to write two chapters as exemplars to be imitated, not as chapters to be kept." Fiction was written; it simply was not kept.

Fix: "covers the first day and a half, in which no fiction that survived was written" or, better, name the throwaway exemplar chapters explicitly so the page agrees with `voice-first.md`.

### 2. `howto/voice-first.md` line 3: "For roughly the first day and a half, the model did not know what the book was about."

Wrong by a factor of roughly fifteen. Session `0c653b33-1efd-45bb-b7ab-26ed3dca981e` starts 2026-08-24T11:52:22Z; turn 18 at 2026-08-24T13:11:27Z is David giving the full concept ("Anyway, here is the concept: The hero is an 18-year old girl who unlocked her class..."). A partial premise arrives even earlier, turn 10 at 12:36. I read the parsed JSON directly and confirmed via `build/parsed/index.json` that this is the chronologically first session, so no earlier and vaguer session rescues the reading.

Fix: "For the first hour and a half of the project's very first session, the model did not know what the book was about."

### 3. `howto/lessons.md` line 5: "The project spent its first day and a half on register with no story in sight"

Overstated, same underlying error as item 2. The story concept arrives about eighty minutes into the first session. `notes/session-summaries.md` line 8 says the same thing: "Once a voice was settled, the real story concept arrived", within the same opening session.

Fix: "The project spent its opening hours on register with no story in sight, and the register it chose is still the book's."

### 4. `howto/the-loop.md` line 11: "David noticed that characters' conversations felt off: too many clever dangling lines, questions answered with non-answers"

Wrong. The 27 August session the page cites is `10c1dd77-c31a-4be9-a7b6-23651a4792b4`. Its only dialogue complaint is turn 14, 2026-08-27T09:52:19Z: "I think Halla is too much like Edwin. it results in a lot of their dialogue blending together and is the root cause of a lot of the conversation sounding abrupt." I scanned every user turn in that session for "clever", "aphoris", "dangling" and "non-answer" and found zero matches. The aphorism and non-answer material belongs to a different thread entirely (`notes/llm-tells.md` and sessions `3ef92e14` and `d1679987`). The page attaches the wrong complaint to the worked example it calls clearest.

Fix: "David noticed that two characters' dialogue, Edwin's and Halla's, was blending together to the point that their conversations sounded abrupt."

### 5. `howto/the-loop.md` line 17: "David's role was described in the project's own notes as adversarial in a useful sense"

Wrong, and a fabricated attribution. I ran `grep -rni "adversarial" /Users/drmaciver/Projects/autoroad` and got 34 hits, every one of them describing an adversarial critique or review process run over the model's own output (sealed-answer critiques in `notes/sealed/*.md`, `notes/decision-principles.md` line 149, `plans/rewrite-readiness.md`), plus unrelated hits in a separate blog-post directory. No note anywhere characterises David's role as adversarial.

Fix: drop the citation and make the point without it, for example "David's feedback consistently pushed back rather than accepting drafts as finished."

### 6. `howto/setup.md` lines 38 to 39: "Ask the model. That sounds glib but it is the honest answer and the one the transcripts show David using."

Wrong as to the attribution. I scanned every string in every file under `build/parsed/` for "terminal", "permission prompt", "what happened" and "why did that fail". All eight matches are model-authored text; no user turn anywhere asks the model to explain a terminal, a failed command, or a permission prompt. David is a fluent technical user throughout. The advice itself is fine; the claim that the transcripts show him taking it is not supported.

Fix: keep the advice and delete the clause "and the one the transcripts show David using".

### 7. `workflow/README.md` line 7: "one discovery move ran a dozen times across fifty-odd scenes, six of them inside a seven-scene stretch"

Overstated and partly invented. Session `3ef92e14-71be-4557-a7d1-f251a7410081` turn 153 records: "Arc 3 had failed it badly, one shape ten times, four inside a single window", and turn 151 locates the drag at chapters 44 to 50. Neither "fifty-odd scenes" nor "six of them inside a seven-scene stretch" appears anywhere in the transcript, and the window-violation count in the source is four, not six.

Fix: "one discovery move ran ten times across Arc 3, four of them inside a single four-scene window, dragging a six-chapter stretch."

### 8. `howto/throwing-away.md` line 11: "two scenes were redrafted from a clean brief that night"; line 29: "The project redrafted two scenes the night of the big discard"

Wrong on both lines. Only scene 23 was drafted and committed that night: commit `5c2debb`, 2026-08-30 19:55, "Act-two redraft, scene 23: rewritten from scratch". The transcript `d1679987` turn 6 ends the night session there, and turn 7 is a new user message the next morning at 2026-08-31T08:19:51Z. Scene 24 was drafted the following morning, commit `c5001ec`, 2026-08-31 09:50. I confirmed the timestamps with `git log --since="2026-08-30 18:00" --until="2026-08-31 08:00"` over `draft/book-01/scenes/`, which returns only the scene 23 commit.

Fix: "one scene was redrafted from a clean brief that night", noting the second followed the next morning if that is wanted.

### 9. `howto/throwing-away.md` line 11: "the overlap checker, built the day before"

Wrong. `git log --follow -- tools/overlap_check.py` returns exactly one creation commit, `f77e026`, 2026-08-30 19:42:26 +0100, four minutes after the rejection commit `2e285ab` at 19:38:52 the same evening. There is no earlier commit for the file.

Fix: "the overlap checker, built minutes earlier that same evening".

### 10. `howto/throwing-away.md` line 21: "it took another day to diagnose the resulting voice drift and restore them"

Wrong. In session `0c653b33`, the seed chapters are deleted at turn 53, 2026-08-24T15:26:29Z, and restored at turn 73, 2026-08-24T17:02:33Z, via `git show 33cc313~1:chapters/001-the-wrong-man.md > samples/seed-chapters/...`. That is one hour and thirty-six minutes later on the same calendar day. I checked the later "restore" mentions on 25 August and they concern unrelated prose fixes in chapter 021.

Fix: "it took a few more hours that same day to diagnose the resulting voice drift and restore them."

### 11. `workflow/overlap-checking.md` line 13: "the project's `CLAUDE.md` explicitly lists the deleted draft directories as ones a session should never open"

Wrong source. I ran `grep -n -i "never open|never read|deleted draft"` over `CLAUDE.md` and got nothing. `CLAUDE.md` lines 53 to 57 only note that the drafts were deleted on 2026-08-31 and now live in git history. The binding prohibition is in `draft/book-01/VOICE.md` section 3.7, lines 166 to 167: "**Never read** `chapters/`, `rewrite/`, `draft/book-01/rejected-act2/`, ...".

Fix: attribute the rule to `VOICE.md` section 3.7 rather than `CLAUDE.md`.

### 12. `workflow/royal-road-publishing.md` line 3: "the project's publishing tool drives that form directly: a headless browser, scripted with Playwright"

Overstated. In `tools/rr/rr.py`, only `cmd_login`, `cmd_whoami` and `cmd_probe` (lines 53 to 107) use `sync_playwright` and `chromium.launch_persistent_context`. Every command that actually publishes, `cmd_create_fiction`, `cmd_update_submission`, `cmd_go`, `cmd_fix_ch1` and `cmd_regroup`, calls `http_session()` at line 118, which is a plain `requests.Session` using saved cookies and antiforgery tokens. Chapter uploads are ordinary HTTP form posts, not browser automation.

Fix: "the project's publishing tool logs in once through a real browser driven by Playwright, then submits the site's own forms directly over HTTP using the saved session, sending what a human filling in the form would send."

### 13. `workflow/next-md-handoff.md` line 9: "run an advisory pass checking that explanations weren't cut for brevity where they shouldn't have been"

Overstated, and the wrong tool. `git show 72261f7:plans/NEXT.md` lists that queue item verbatim as "a `because` pass over 101 to 118 like the one run on 90 to 100". The subagent instruction in `build/parsed/subagents/af9d8c86b2be3dad3.json` confirms it is mechanical prose-tic thinning: count "because" per scene, get every scene under four per thousand words, "Keep every reason; change the joint", plus a parallel write-verb tic pass. The advisory brevity check described is a different, already-completed step, the `pre-david-pass` skill. The other four queue items match `plans/NEXT.md` in order.

Fix: "run a mechanical pass thinning overused 'because' constructions and write-verb tics in the newest chapters, keeping every reason intact".

### 14. `howto/delegation.md` line 9: the 27 August "house policy"

Overstated, and it conflates two pieces of feedback two days apart. The 27 August feedback, session `10c1dd77` turn at 08:16:05Z, is entirely about model choice and budget: "You're running subagents as fable again and as a result have burned through the entire remainder of the fable budget for this week. Please restart that workflow using opus at most, and sonnet where appropriate." That became commit `04c6c8b`, which adds only the never-run-on-Fable rule and the opus-versus-sonnet split. Nothing there says to stop reaching for subagents for small tasks or to keep interactive work in the main session. The broader "stop running fable subagents for everything" line is from 25 August, session `0c653b33` at 10:49:42Z, and his very next turn at 10:51:06Z says the opposite of the page's gloss: "In general, please do *most* work in subagents and workflows, and keep fable for only this session."

Fix: describe the 27 August policy as it was, never run subagents on Fable, opus for judgement-heavy work and sonnet for mechanical passes, and cite the 25 August instruction separately if it is wanted.

### 15. `workflow/canon-and-claim-levels.md` line 18: "If canon and an earlier accepted chapter turn out to disagree, both get flagged, and the decision belongs to David rather than to the model"

Overstated. `.claude/skills/consistency-check/SKILL.md` line 37 governs exactly this case and resolves it automatically: "If canon and an earlier chapter conflict, canon wins; flag the earlier chapter too." David's authority is reserved for a different question, whether a canon entry may be weakened or deleted to accommodate a draft.

Fix: "If canon and an earlier accepted chapter turn out to disagree, canon wins and the earlier chapter is flagged for revision, rather than the model quietly editing canon to fit what was already written."

### 16. `howto/voice-first.md` line 11: "It was written before a word of the actual novel existed."

Wrong as stated, because the preceding sentence characterises the document by an item that was added late. `notes/llm-tells.md` was created at commit `65f34c5`, 2026-08-24 13:23:07, before any chapter. But the arithmetic-metaphor tell named in the preceding sentence was added at commit `1bb6f7d`, 2026-08-24 20:26:34, one minute after chapter 018 was committed (`576a2db`, 20:25:27), with eighteen chapters and about 64,000 words already drafted. The session text says so directly: "28 uses in ~64k words, spread across 15 of 18 drafted chapters".

Fix: "The core of that list was written before a word of the actual novel existed, though items like the arithmetic-metaphor tell were added later, once drafting was well underway."

### 17. Contradiction: `workflow/farming-facts-and-author-notes.md` line 13 mislabels transcript `c214c046`

The page links to `../transcripts/c214c046-1bb3-4385-abee-f924d8349bad.md` with the link text "2026-08-31, redrafting scene by scene". That transcript is not the redraft. Its first user turn, 2026-08-31T08:42:33Z, reads "In the canon, can you build an actual map (as svg) of the area covered by book 1?", and the session is eight turns and nineteen minutes long with no redrafting in it. `chronicle/2026-08-31.md` agrees, listing it separately as "map addition" and pointing the scene-by-scene redraft at `d1679987`. Note that `site/src/transcripts/titles.json` also mislabels `c214c046`, apparently swapped with `d1679987`, but the transcript itself and the chronicle page outrank it.

Fix: change the link text to "2026-08-31, mapping the setting", and correct `titles.json` separately.

### 18. Contradiction: `workflow/overlap-checking.md` gets the order of cleanup and acceptance backwards

The page says the discarded drafts "were deleted from the working tree entirely as part of a repository cleanup once the third draft was accepted as the real one". The commit history says the reverse. Commit `275198e`, "Repo cleanup + commenter rework for publication review", is dated 2026-08-31 11:43:51 +0100, the first commit of that day, and its own message explains the purpose: the overlap checker reads the old drafts from git history at the pin "so the mirroring test works with nothing on disk". The act-two redraft that produced the accepted third draft ran after it, and the book only went live at the end of that day per `chronicle/2026-08-31.md`. The deletion enabled the redraft; it did not follow its acceptance.

Fix: "deleted from the working tree as part of a repository cleanup on the morning of 31 August, done so the overlap checker could run against git history instead of live files during that day's scene-by-scene redraft".

### 19. Contradiction: the sealed-answer rule is absolute on two pages and conditional on a third

`CLAUDE.md` lines 112 to 114 state the rule with an explicit exception: "**Never tell DRMacIver what a sealed answer is**, in prose, summary, hint, commit message, or 'harmless' paraphrase, unless he very specifically asks for spoilers in that message." `workflow/claude-md-rules.md` line 13 reflects that correctly ("never disclosed to David except on request"). But `howto/write-it-down.md` line 15 says "never shown to David" and `howto/delegation.md` line 15 says "therefore never reach David", both flatly absolute. All three cannot be right.

Fix: add the qualifier on both howto pages, for example "kept from David by default ... unless he specifically asks to be spoiled".

### 20. Contradiction: the census chapter range differs between two pages

`chronicle/2026-08-25.md` line 9 says the language census compared "chapters 1 to 21". The source note, written by the census subagent and committed as `cd5fcd2` ("Language guide: modifications from the oddity census"), says: "Twenty-three readers gathered \"sounds off\" lines across chapters 1 to 23 (~93k words)." `workflow/llm-tells-and-linting.md` line 7 cites the same event by the same 23 readers and 93,000 words. Two ranges for one census.

Fix: change `chronicle/2026-08-25.md` to "chapters 1 to 23".

### 21. Contradiction: `about.md` states the file-contents redaction rule with no exception, but `howto/voice-first.md` relies on one

`about.md` says the rule "is applied blind" and that novel prose, canon files and sealed answers are "never shown". `howto/voice-first.md` line 13 says "Everything before the premise is shown unredacted in the transcript, sample scenes included". I checked the rendered transcript `site/src/transcripts/0c653b33-1efd-45bb-b7ab-26ed3dca981e.md`: before the premise reveal at roughly line 2189, the only redactions are private filesystem paths, so `voice-first.md` is right and `about.md` is unscoped. `introduction.md` sends readers to `about.md` as the full policy, so the gap matters.

Fix: scope the File contents paragraph in `about.md` to note the pre-premise exception and link to `voice-first.md`.

### 22. Drift, but worth fixing: `howto/delegation.md` links the overnight first draft to the wrong chronicle day

The page says "The [first](../chronicle/2026-08-24.md) produced the first complete draft of book one overnight." The 24 August chronicle page only says drafting on the first arc "was underway" by end of day; the completed manuscript is `chronicle/2026-08-25.md`: "the whole of book one, all three arcs, got drafted, revised, and assembled into a complete manuscript". Session `0c653b33` does span both days, so the claim is not false, but a reader following the link lands on a page that does not support it.

Fix: point the link at `../chronicle/2026-08-25.md`.

## Unverifiable claims

Twenty-nine claims could not be settled against the sources. Twenty-five are unverifiable in principle from the available record; four were left unchecked for effort reasons and are flagged as such.

Claims about people outside the project, which the transcripts cannot evidence at all. `introduction.md` line 3, "Enough people asked him how that actually worked". `howto/README.md` line 3, "Most people who asked David how the novel was made were not asking for a tour of his repository." `howto/the-loop.md` line 3, "The question people most often asked was some version of 'but what do you actually say to it?'" `howto/checks.md` line 17, "the last two are the ones people do not expect". `howto/checks.md` line 7, "the one most people could set up in an afternoon". To confirm any of these the author would need a record outside the sessions, or should mark them as his own impression rather than a finding.

Claims about David's circumstances that sessions do not record. `howto/setup.md` line 7, the "Claude Max subscription": all nine sessions confirm a Mac, a terminal and a single project folder via their `cwd`, but transcripts carry no billing or plan information. `howto/setup.md` line 17, "which is why David was on the largest individual plan and still watched his budget": same problem, no plan or usage data appears anywhere in the record. `howto/README.md` line 5, "someone who writes software for a living and had used Claude Code heavily before": strongly consistent with the observed behaviour, never stated. The author can confirm these from his own knowledge; they simply cannot be sourced from the material this check has.

Absolute claims about the site's own provenance. `about.md` line 5, "every page of prose here, including this one, came out of a model rather than a person". The build pipeline makes this highly likely, but confirming "every page" would need an audit of each page's generation, which this check does not have access to.

Editorial and evaluative framings with no factual referent. `introduction.md` line 21, "it is a record of what happened rather than of what anyone intended". `howto/README.md` line 15, "argues that this was the best decision in the project". `howto/voice-first.md` line 5, "Every later scene inherits the register the project settled into early, so the register is where the effort has the most leverage." `howto/write-it-down.md` line 3, "This is the constraint that shaped the project's whole structure more than any other", a superlative no source ranks. `howto/write-it-down.md` line 3, "a decision you made together but did not record has not, for practical purposes, been made", a maxim rather than an event. `howto/checks.md` line 21, "This alone removes a surprising amount of the generated feel", a magnitude nothing measures. To keep these, soften them to explicitly authorial statements.

Distributional claims that were never counted. `howto/the-loop.md` line 19, "Feedback that did not work as well tended to be aesthetic without a reason attached": verifying this would mean categorising every feedback exchange across ten days. `howto/write-it-down.md` line 19, "Almost every rule in the project's files exists because of a specific earlier mistake": the pattern is real and common, dated rulings with reasons appear throughout, but "almost every" would need an audit of all rules. Soften to "many rules" unless that audit is done.

Causal claims whose chain was not traced. `howto/the-loop.md` line 23, "Neither of those happened by accident", about the 28 and 31 August self-catches. `howto/write-it-down.md` line 21, "a new session inherits not just the rules but the reasons". `howto/write-it-down.md` line 13, the "three chapters" figure in "once it has done that in three chapters the assumption is settled": the claim-level system is real, the specific number is not sourced, and a non-numeric phrasing would be safer.

Attribution I could not find the source for. `howto/the-loop.md` line 17, "largely to catch places where the model's quality bar had slipped", attributed to the project's notes. I grepped `notes/*.md`, `CLAUDE.md` and `VOICE.md` for this framing and found nothing. The behaviour is visible in the transcripts; the self-description is not.

Prescriptive advice in the "Steps you can take" sections, which is not a claim about the transcripts at all and has nothing to check it against: `howto/write-it-down.md` lines 28, 29 and 30 ("ask whether that is decided or assumed"; "Do not let assumptions harden by repetition"; "end the exchange by asking the model to write it into the relevant file"; "If you do not, you will be giving the same feedback next week"). Flagged only so the author can confirm these are meant as advice rather than as descriptions of what David did.

One claim needing a literary judgement rather than a receipt. `howto/lessons.md` line 5, "the register it chose is still the book's". Settling this means comparing the first session's register against the finished manuscript end to end. Marking it as the project's self-report would make it safe.

Unchecked, for effort reasons rather than in principle, all in `howto/lessons.md`: line 19, "The knowledge from each was in the rule files before the draft went", which needs each discard's rule-extraction timestamps traced against its discard date; line 23, "the unattended runs had a written stopping rule", where `plans/NEXT.md` does show "an independent quality read every couple of chapters and a stop if it degraded" but I did not confirm it was written before the run or check every unattended run; and lines 27, "The five-book plan, the first draft, the first set of voice rules" and "The parts that lasted were the ones that came out of a specific failure", which need a systematic revision-history comparison across `plans/series.md`, the first draft and the first voice-rules set.

## Drift and ambiguity

Twenty-six findings where the claim is essentially right but the wording strains against the source. These are not errors; each is a place where a small edit would make the page match the record more exactly.

Numbers and rates. `howto/checks.md` line 9, "eleven per chapter in drifted prose and four in good prose": `notes/voices.md` gives "~280 trailing 'which' glosses in 93k words (about 11 per chapter). The seed has four 'which' clauses in 2,700 words". The eleven is exact; the four is a total in one sample, not a per-chapter rate. `chronicle/README.md` line 15, "dozens of them", where two other pages give the precise 110 fabricated quotations; "over a hundred" would match. `howto/the-loop.md` line 11, "one late test assigned every line correctly": true of raw attribution (86 percent and 100 percent in round four), but the same turn reports 3/6 and 2/6 on the stricter swap test, which the sentence does not mention.

Scope. `howto/checks.md` line 7, "a small Python linter that runs in seconds and never disagrees with itself": true of the regex and metric tiers that `prose_lint.py` actually runs, but the catalogue's semantic tier goes through the model pipeline instead, so the sentence should name the tiers. `howto/the-loop.md` line 13, "that one sentence became a policy that shaped every later scene": the correction was written into four canon files immediately, which is confirmed; "every later scene" is stronger than anything checked.

Unsupported clauses attached to otherwise accurate rules. `workflow/README.md` line 7, "unless it's one continuous action": the four-scene engine rule is confirmed near verbatim in `notes/process.md` lines 75 to 78, but I grepped `notes/` and `plans/` for "continuous action" and got no matches anywhere, so the exception appears to be invented. `workflow/canon-and-claim-levels.md` line 17, "softer thematic consistency last": theme is explicitly called softer in the skill, but it is not literally last in either list.

Paraphrases presented as if quoted. `workflow/voice-and-exemplars.md` line 11, "Rules exist to annotate the exemplars": a fair summary of `VOICE.md`, not a line in it. `workflow/voice-and-exemplars.md` line 17, the "don't listen perfectly" rationale, which is synthesised across `notes/voices.md` rule 8 and `notes/llm-tells.md` tell 6. `howto/setup.md` line 27, the quoted "commit what we have so far with a sensible message", which is illustrative; the underlying claim is confirmed by over a hundred model-authored commits. `howto/setup.md` line 31, "a resumed conversation is not the same as a remembered one", the author's framing of a pattern that the transcripts do clearly show. `howto/write-it-down.md` line 15, "so that he reads the book as a reader would": `CLAUDE.md`'s stated reason is that the terminal shows him every tool diff, which amounts to the same intent.

Timings that are right in kind but loose in degree. `howto/voice-first.md` line 19, "spent a day recovering from the voice drift": the fix landed one hour and thirty-six minutes later the same afternoon. `workflow/next-md-handoff.md` line 15, canon files "which do keep dated history at the bottom": the dated rulings are real but interleaved through `notes/canon/characters/*.md`, not gathered at the foot. `howto/write-it-down.md` line 27, "Keep a handoff document from the first day": good advice, but `plans/NEXT.md` was first committed 2026-08-29, five days into the project, so it should not be read as a description of what happened here.

Sequencing. `chronicle/2026-08-26.md`, "already been established": the green-revolution framing does predate 26 August (canon citations dated 2026-08-24), but the specific parish-ceiling rule about multiplying or speeding up labour was formalised during that same 26 August session.

Small ones, listed for completeness because the underlying claim is confirmed and only the phrasing wobbles: `howto/voice-first.md` line 9 "None were kept" (the practitioner direction did carry forward even though the samples did not); `howto/voice-first.md` line 9 "roughly the voice the published book has now" (the name persists across the whole corpus, which is as close as the record gets); `howto/voice-first.md` line 11's arithmetic example, covered under problem 16; `howto/the-loop.md` lines 7 and 7, "Usually that is a scene or a chapter" and "sometimes it is a planning document", both well attested but qualitative; `howto/the-loop.md` line 11, the "characters do not listen perfectly" standing rule, where the actual documented mechanisms are the diagnostic mishearing and the wrong guess about the other's reasoning; `howto/the-loop.md` line 23, "Both followed periods where David had made clear that he wanted problems surfaced rather than smoothed over", where the contamination self-stop is confirmed verbatim but that exact characterisation of David's instruction is an inference; `howto/the-loop.md` line 11 "The first round scored badly", where no discrete round-one figure appears in the transcript and the explicit numbers reported afterwards belong to round two; and the delegation link drift covered under problem 22.

## Claim table

Grouped by page. Verdict key: C confirmed, CN confirmed with nuance, U unverifiable, X unchecked, O overstated, W wrong. Verification column names the receipt.

### introduction.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 1 | introduction.md:3 | published on Royal Road | publishing/blurb.md, fiction.json, rr-map.json | C |
| 2 | introduction.md:3 | written with Claude Code | index.json, 9 sessions; git trailers | C |
| 3 | introduction.md:3 | enough people asked | no source possible | U |
| 4 | introduction.md:7 | every word generated by Claude | pipeline in tools/ | C |
| 5 | introduction.md:7 | David set rules and direction | transcript turn shapes | C |
| 6 | introduction.md:7 | includes this paragraph | pipeline | C |
| 7 | introduction.md:11 | still being published | plans/NEXT.md 2026-09-02 | C |
| 8 | introduction.md:11 | redacted against spoilers | tools/redact.py | C |
| 9 | introduction.md:11 | two names survive | grep over rendered transcripts | C |
| 10 | introduction.md:11 | both on the published page | grep publishing/blurb.md | C |
| 11 | introduction.md:12 | file contents never shown | redact.py allowlist; rendered output | C |
| 12 | introduction.md:12 | only the fact of a read or write | same | C |
| 13 | introduction.md:15 | four sections | site tree | C |
| 14 | introduction.md:15 | same ten days | index.json span 08-24 to 09-02 | C |
| 15 | introduction.md:21 | 24 Aug to 2 Sep | git history | C |
| 16 | introduction.md:21 | reconstructed from commits and transcripts | pipeline | C |
| 17 | introduction.md:21 | record of what happened | editorial | U |
| 18 | introduction.md:21 | much was thrown away | git history of discards | C |
| 19 | introduction.md:23 | long, unedited | wc -l, 18037 lines total | C |
| 20 | introduction.md:25 | pages link to each other | link pre-pass, 83/83 | C |

### about.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 21 | about.md:5 | Claude did all of it | transcript turn shapes | C |
| 22 | about.md:5 | scripts read git history and transcripts | parse_transcripts.py, prose_index.py | C |
| 23 | about.md:5 | every page came out of a model | not auditable here | U |
| 24 | about.md:7 | direction and redaction | transcript turn shapes | C |
| 25 | about.md:7 | he did not write the pages | same | C |
| 26 | about.md:7 | pipeline sees only what was recorded | pipeline architecture | C |
| 27 | about.md:11 | a chapter a day | publishing/chapters.json, rr-map.json | C |
| 28 | about.md:11 | readers in the middle | same | C |
| 29 | about.md:11 | scenes 1 to 40 published | chapters.json, 18 chapters | C |
| 30 | about.md:11 | everything else a spoiler | chapters.json vs scene 118 | C |
| 31 | about.md:13 | only two names survive | spoilers.json, rendered transcripts | C |
| 32 | about.md:13 | both already public | blurb.md | C |
| 33 | about.md:15 | topics matched by pattern | spoilers.json topic_regexes | C |
| 34 | about.md:17 | scene numbers visible as filenames | redact.py _mark_scene_numbers | C |
| 35 | about.md:17 | tagged unpublished, contents never appear | redact.py, prose_index.py | C |
| 36 | about.md:19 | shows that it happened, not what was in it | redact.py allowlist | C |
| 37 | about.md:19 | prose and canon pass through constantly | grep over transcripts | C |
| 38 | about.md:19 | none ever shown | redact.py blind rule | C (but see problem 21) |
| 39 | about.md:21 | local paths removed | redact.py lines 47 to 54 | C |
| 40 | about.md:21 | repository not named | site grep | C |
| 41 | about.md:25 | ordinary words over-redacted | spoilers.json terms, word-boundary regex | C |
| 42 | about.md:25 | topic patterns catch innocent uses | topic_regexes applied blind | C |
| 43 | about.md:25 | both happen on this site | same | C |
| 44 | about.md:25 | left alone rather than hand-tuned | no exception mechanism in redact.py | C |
| 45 | about.md:27 | a word probably has been cut | redaction markers | C |
| 46 | about.md:27 | occasionally a whole exchange | rendered transcripts | C |
| 47 | about.md:31 | royalroad.com/fiction/189685 | commit 614c303 | C |
| 48 | about.md:31 | openly labelled AI-written | blurb.md | C |
| 49 | about.md:31 | the point from the first day | 0c653b33 turn 0 | C |

### howto/README.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 50 | howto/README.md:3 | what most askers wanted | no source | U |
| 51 | howto/README.md:5 | one project, ten days | index.json | C |
| 52 | howto/README.md:5 | writes software for a living | not stated in record | U |
| 53 | howto/README.md:5 | site generated by the model | pipeline | C |
| 54 | howto/README.md:9 | tools are residue of failures | git history | C |
| 55 | howto/README.md:9 | planned parts largely thrown away | git history | C |
| 56 | howto/README.md:15 | first day and a half, no fiction | commit b6cd810 | W |
| 57 | howto/README.md:15 | argues best decision | editorial | U |
| 58 | howto/README.md:21 | over a hundred fabricated quotations | 110, commit 135e34d | C |
| 59 | howto/README.md:25 | supervision changed | Agent counts by session | C |

### howto/setup.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 60 | howto/setup.md:7 | Mac, terminal, Claude Max | cwd in all 9 sessions; plan unsourced | CN |
| 61 | howto/setup.md:7 | Markdown files under git | git ls-files, 410 .md | C |
| 62 | howto/setup.md:7 | every conversation in that folder | cwd identical in all sessions | C |
| 63 | howto/setup.md:7 | not the only setup | general | U |
| 64 | howto/setup.md:7 | probably not the easiest | general | U |
| 65 | howto/setup.md:11 | desktop app, Linux beta | code.claude.com/docs/en/setup | C |
| 66 | howto/setup.md:11 | same engine | docs | C |
| 67 | howto/setup.md:11 | no terminal required | docs | C |
| 68 | howto/setup.md:11 | open folder, chat panel, review visually | docs quickstart | C |
| 69 | howto/setup.md:11 | handles git if asked | docs | C |
| 70 | howto/setup.md:13 | CLI slightly easier for scripts | site cross-ref | C |
| 71 | howto/setup.md:13 | model runs them either way | Bash counts per session | C |
| 72 | howto/setup.md:17 | Pro, Max, Team, Enterprise, API credits | docs | C |
| 73 | howto/setup.md:17 | free tier excluded | docs | C |
| 74 | howto/setup.md:17 | check the pricing page | link resolves | C |
| 75 | howto/setup.md:17 | rolling windows | docs | C |
| 76 | howto/setup.md:17 | largest individual plan, watched budget | no plan data in record | U |
| 77 | howto/setup.md:19 | git present on Mac, git-scm.com for Windows | docs, link | C |
| 78 | howto/setup.md:19 | Claude Code can talk you through it | docs | C |
| 79 | howto/setup.md:23 | installers documented at setup page | docs | C |
| 80 | howto/setup.md:23 | Terminal via Spotlight | general | C |
| 81 | howto/setup.md:25 | work stays inside the folder | docs | C |
| 82 | howto/setup.md:27 | /init drafts CLAUDE.md | docs memory page | C |
| 83 | howto/setup.md:27 | no git commands needed | 100+ model-authored commits; quote illustrative | CN |
| 84 | howto/setup.md:29 | asks before changing files | docs permission-modes | C |
| 85 | howto/setup.md:29 | approving everything is normal | general | U |
| 86 | howto/setup.md:29 | plan mode exists | docs | C |
| 87 | howto/setup.md:29 | Shift and Tab | docs | C |
| 88 | howto/setup.md:31 | sessions end on close | docs | C |
| 89 | howto/setup.md:31 | /resume and claude -c | docs | C |
| 90 | howto/setup.md:31 | resumed is not remembered | 3ef92e14 turns 144, 315 | CN |
| 91 | howto/setup.md:35 | record kept in .claude | docs | C |
| 92 | howto/setup.md:35 | generated by scripts, redacted, rendered | tools/ and build/ | C |
| 93 | howto/setup.md:35 | source public on GitHub | link | C |
| 94 | howto/setup.md:35 | records contain everything | general | C |
| 95 | howto/setup.md:38 | the transcripts show David asking | zero matches in user turns | W |
| 96 | howto/setup.md:39 | Claude Code can explain terminals | docs; general capability | C (finding rejected) |
| 97 | howto/setup.md:39 | first hour is the hardest | general | U |

### howto/voice-first.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 98 | voice-first.md:3 | first thing was not the novel | 0c653b33 turn 0 | C |
| 99 | voice-first.md:3 | first day and a half without the premise | turn 18 at 13:11, 80 minutes in | W |
| 100 | voice-first.md:3 | the destination | turn 0 verbatim | C |
| 101 | voice-first.md:5 | default voice most recognisable | editorial | C |
| 102 | voice-first.md:5 | later scenes inherit the register | interpretive | U |
| 103 | voice-first.md:9 | first session opens with research | turn 1, WebSearch | C |
| 104 | voice-first.md:9 | two webfiction books studied | turns 2, 3, 15 | C |
| 105 | voice-first.md:9 | three voices, none kept | turns 1, 2; direction did carry | CN |
| 106 | voice-first.md:9 | Wry Practitioner | turn 3 | CN |
| 107 | voice-first.md:11 | tells document built | notes/llm-tells.md turn 5; arithmetic added later | CN |
| 108 | voice-first.md:11 | tightened repeatedly | turns 5, 101, 103; census | C |
| 109 | voice-first.md:11 | written before a word of the novel | commit 1bb6f7d after ch 018 | W |
| 110 | voice-first.md:13 | premise then two exemplar chapters | turns 17 to 19 | C |
| 111 | voice-first.md:13 | pre-premise shown unredacted | rendered transcript to line 2189 | C |
| 112 | voice-first.md:19 | deleted exemplars, spent a day recovering | same-day, 1h36m | CN |
| 113 | voice-first.md:19 | chronicle link | file exists | C |
| 114 | voice-first.md:20 | exemplar wins over rule | VOICE.md line 36 | C |
| 115 | voice-first.md:24 | rules alone read generic | turn 73 verbatim | C |
| 116 | voice-first.md:24 | rules annotate examples | VOICE.md stance | C |

### howto/the-loop.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 117 | the-loop.md:3 | the question people most often asked | no source | U |
| 118 | the-loop.md:7 | a round starts with David reading | many sessions | CN |
| 119 | the-loop.md:7 | sometimes a planning document | 0c653b33 turn 157; 3ef92e14 turn 277 | CN |
| 120 | the-loop.md:11 | dialogue work on 27 August | session 10c1dd77 | C |
| 121 | the-loop.md:11 | clever dangling lines, non-answers | actual complaint was Halla vs Edwin | W |
| 122 | the-loop.md:11 | model proposed a test | turn 15 | C |
| 123 | the-loop.md:11 | strip speaker names | turn 15, turn 21 | C |
| 124 | the-loop.md:11 | first round scored badly | no discrete round-one figure | U |
| 125 | the-loop.md:11 | one late test assigned every line | turn 25; swap test 2/6 | CN |
| 126 | the-loop.md:11 | per-character countable constraints | notes/dialogue-voices.md | CN |
| 127 | the-loop.md:13 | return on labour correction | turns 157, 158 verbatim | C |
| 128 | the-loop.md:13 | shaped every later scene | policy in 4 files; "every" unchecked | CN |
| 129 | the-loop.md:13 | author's notes reworked | turns 163, 164 | C |
| 130 | the-loop.md:13 | persona document | turn 164; d1679987 turn 46 | C |
| 131 | the-loop.md:17 | across the ten days | index.json | C |
| 132 | the-loop.md:17 | notes call his role adversarial | grep, 34 hits, none match | W |
| 133 | the-loop.md:17 | catching quality-bar slips | source not found | U |
| 134 | the-loop.md:19 | feedback that did not work | never counted | U |
| 135 | the-loop.md:19 | examples of both | site cross-ref | C |
| 136 | the-loop.md:23 | 31 Aug contamination stop | d1679987 verbatim | C |
| 137 | the-loop.md:23 | 28 Aug scoring retraction | chronicle, 10c1dd77 turn 21 | C |
| 138 | the-loop.md:23 | neither by accident | causal, untraced | U |
| 139 | the-loop.md:23 | rule files said so in writing | CLAUDE.md flagging rules | CN |

### howto/write-it-down.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 140 | write-it-down.md:3 | no memory of the previous session | docs | C |
| 141 | write-it-down.md:3 | it knows because a file told it | docs, CLAUDE.md | C |
| 142 | write-it-down.md:3 | shaped the structure more than any other | superlative | U |
| 143 | write-it-down.md:3 | a rule in conversation binds that conversation | docs | C |
| 144 | write-it-down.md:3 | unrecorded decisions are not made | maxim | U |
| 145 | write-it-down.md:7 | every session reads CLAUDE.md | docs memory page | C |
| 146 | write-it-down.md:7 | a pointer file | CLAUDE.md structure | C |
| 147 | write-it-down.md:7 | lists what to read, and why | CLAUDE.md items 0 to 7 | C |
| 148 | write-it-down.md:9 | three files worth calling out | NEXT.md, canon, sealed | C |
| 149 | write-it-down.md:11 | plans/NEXT.md handoff | NEXT.md line 1 | C |
| 150 | write-it-down.md:11 | state as of a date, numbered queue | NEXT.md line 3 | C |
| 151 | write-it-down.md:11 | closed items deleted | git log -p diffs | C |
| 152 | write-it-down.md:13 | Established, Working, Open | canon files | C |
| 153 | write-it-down.md:13 | Working hardens over three chapters | number unsourced | U |
| 154 | write-it-down.md:15 | sealed files subagent-written | CLAUDE.md 108 to 119 | C |
| 155 | write-it-down.md:15 | so he reads as a reader | stated reason is tool diffs | CN |
| 156 | write-it-down.md:15 | the silent-soil failure | CLAUDE.md 100 to 106 | C |
| 157 | write-it-down.md:15 | the state is not reachable | CLAUDE.md 100 to 101 | C |
| 158 | write-it-down.md:19 | almost every rule from a mistake | pattern real, "almost every" uncounted | U |
| 159 | write-it-down.md:19 | file records rule and mistake | dated rulings in canon | C |
| 160 | write-it-down.md:19 | inherits rules and reasons | inference | U |
| 161 | write-it-down.md:21 | opinion versus checkable rule | rules.json structure | C |
| 162 | write-it-down.md:21 | endings rule can be tested for | CLAUDE.md; rules.json fragment-closer-budget | C |
| 163 | write-it-down.md:25 | start a repository | advice | C |
| 164 | write-it-down.md:27 | handoff from the first day | NEXT.md first committed 08-29 | CN |
| 165 | write-it-down.md:27 | update at end of every session | 19 commits, structure | C |
| 166 | write-it-down.md:28 | ask decided or assumed | advice | U |
| 167 | write-it-down.md:28 | do not let assumptions harden | advice | U |
| 168 | write-it-down.md:29 | write feedback into the file | advice | U |
| 169 | write-it-down.md:30 | otherwise you repeat yourself | advice | U |
| 170 | write-it-down.md | four internal links | files exist | C |

### howto/checks.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 171 | checks.md:7 | just over a hundred rules | 110 in rules.json | C |
| 172 | checks.md:7 | small deterministic linter | prose_lint.py, regex and metric tiers only | CN |
| 173 | checks.md:7 | least glamorous thing | editorial | C |
| 174 | checks.md:7 | most could set it up in an afternoon | no source | U |
| 175 | checks.md:9 | the verdict clause | llm-tells.md 182 to 185 | C |
| 176 | checks.md:9 | eleven per chapter, four in good prose | voices.md; four is a sample total | CN |
| 177 | checks.md:9 | budgets moved to per 1,000 words | voices.md ruled 2026-08-28 | C |
| 178 | checks.md:11 | fan-out, one call per rule group per file | language-police SKILL.md | C |
| 179 | checks.md:11 | fan-out then judge recurs | SKILL.md, workflow/README.md | C |
| 180 | checks.md:11 | linting page link | file exists | C |
| 181 | checks.md:13 | citation checker verifies quotations | check_citations.py | C |
| 182 | checks.md:13 | 206 mismatches | commit 135e34d, 3ef92e14 turn 114 | C |
| 183 | checks.md:13 | 110 never written | same turn | C |
| 184 | checks.md:13 | problem was in the notes | turn 114 examples | C |
| 185 | checks.md:13 | eight or more shared words | overlap_check.py n=8 | C |
| 186 | checks.md:13 | never in a working tree | overlap_check.py PIN | C |
| 187 | checks.md:17 | four families of catch | four checks attested | C |
| 188 | checks.md:17 | any long project hits all four | general | C |
| 189 | checks.md:17 | last two are unexpected | no source | U |
| 190 | checks.md:21 | removes a surprising amount | unmeasured | U |
| 191 | checks.md:25 | rejected findings logged | 110 counter_examples entries | C |
| 192 | checks.md:25 | not proposed again | judge prompt includes counter-examples | C |

### howto/throwing-away.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 193 | throwing-away.md:3 | the book is the third draft | git history | C |
| 194 | throwing-away.md:3 | first draft on the second day | 0c653b33 into 08-25 | C |
| 195 | throwing-away.md:3 | reclassified on the fourth | chronicle, git | C |
| 196 | throwing-away.md:3 | sixty-five scenes in act two | 25 to 31 and 34 to 89 | C |
| 197 | throwing-away.md:3 | drafted in a single push 30 Aug | git | C |
| 198 | throwing-away.md:3 | pulled the same evening | commit 2e285ab 19:38 | C |
| 199 | throwing-away.md:3 | neither will be read | site cross-ref | C |
| 200 | throwing-away.md:3 | both were necessary | editorial | C |
| 201 | throwing-away.md:5 | most are not assets | editorial | C |
| 202 | throwing-away.md:9 | by 27 Aug fixing cost more | chronicle 08-27 | C |
| 203 | throwing-away.md:9 | chronicle link | file exists | C |
| 204 | throwing-away.md:11 | act drafted with checks passing 30 Aug | git | C |
| 205 | throwing-away.md:11 | overlap checker built the day before | commit f77e026, same evening | W |
| 206 | throwing-away.md:11 | new prose too close to rejected material | commit f77e026 message | C |
| 207 | throwing-away.md:11 | two scenes redrafted that night | only scene 23 | W |
| 208 | throwing-away.md:15 | census and overlap are corpus-level | tool sources | C |
| 209 | throwing-away.md:21 | exemplars deleted on the first day | turn 53 | C |
| 210 | throwing-away.md:21 | another day to restore | 1h36m same day | W |
| 211 | throwing-away.md:28 | overlap page link | file exists | C |
| 212 | throwing-away.md:29 | redrafted two scenes that night | only scene 23 | W |

### howto/delegation.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 213 | delegation.md:3 | three scales of work | docs | C |
| 214 | delegation.md:3 | the project used all three | git, transcripts | C |
| 215 | delegation.md:7 | drafting stayed in the main session | VOICE.md 133 to 136 | C |
| 216 | delegation.md:7 | character-voice subagent experiment | session-summaries.md line 22 | C |
| 217 | delegation.md:9 | 27 August house policy | actual policy was Fable and model choice | O |
| 218 | delegation.md:13 | bounded checks to subagents | skills, Agent counts | C |
| 219 | delegation.md:15 | sealed work by subagents only | CLAUDE.md 108 to 119 | C, but see problem 19 |
| 220 | delegation.md:15 | delegation as information barrier | CLAUDE.md rationale | C |
| 221 | delegation.md:19 | several hundred review agents 31 Aug | Agent counts | C |
| 222 | delegation.md:19 | one cheap agent per chapter | consistency workflow | C |
| 223 | delegation.md:21 | the first produced the draft overnight | link points at 08-24, event is 08-25 | CN |
| 224 | delegation.md:21 | the last drafted the rest in under three hours | 7257e15f session span | C |
| 225 | delegation.md:21 | rules in files made it possible | site cross-ref | C |
| 226 | delegation.md:25 | gated pipeline on 31 Aug | d1679987 | C |
| 227 | delegation.md:25 | gate loosened through the day | d1679987 | C |
| 228 | delegation.md:25 | two days later unattended | 7257e15f | C |
| 229 | delegation.md:29 to 32 | four pieces of advice | advice, grounded in the above | C |

### howto/lessons.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 230 | lessons.md:3 | farming fantasy in ten days | git span | C |
| 231 | lessons.md:5 | first day and a half on register | concept at 80 minutes | O |
| 232 | lessons.md:5 | the register is still the book's | needs literary comparison | U |
| 233 | lessons.md:5 | first session link | file exists | C |
| 234 | lessons.md:7 | rules alone produced generic prose | turn 73 | C |
| 235 | lessons.md:7 | exemplars produced the voice | turn 73 | C |
| 236 | lessons.md:7 | voice drift 24 and 25 Aug | turns 53, 73 | C |
| 237 | lessons.md:9 | blind tests to countable constraints | 10c1dd77 | C |
| 238 | lessons.md:9 | 27 Aug link | file exists | C |
| 239 | lessons.md:11 | sessions have no memory | docs | C |
| 240 | lessons.md:11 | handoff, pointer, dated rulings | NEXT.md, CLAUDE.md, voices.md | C |
| 241 | lessons.md:11 | last session read the queue | 7257e15f first turn | C |
| 242 | lessons.md:13 | 206 and 110 | commit 135e34d | C |
| 243 | lessons.md:13 | 28 Aug link | file exists | C |
| 244 | lessons.md:15 | discards caused by properties of the whole | transcripts | C |
| 245 | lessons.md:15 | no per-scene check could see | tool sources | C |
| 246 | lessons.md:15 | 30 Aug link | file exists | C |
| 247 | lessons.md:17 | fan-out then judge | language-police SKILL.md | C |
| 248 | lessons.md:17 | cheaper, not worse on seeded tests | pilot-report.md | C |
| 249 | lessons.md:17 | linting page link | file exists | C |
| 250 | lessons.md:19 | two drafts thrown away | git | C |
| 251 | lessons.md:19 | knowledge was in the rule files first | not traced | X |
| 252 | lessons.md:19 | throwing away link | file exists | C |
| 253 | lessons.md:21 | splitting drafting lost coherence | VOICE.md | C |
| 254 | lessons.md:21 | splitting checks gained speed | skills | C |
| 255 | lessons.md:21 | delegation link | file exists | C |
| 256 | lessons.md:23 | scene by scene to unattended over four days | d1679987, 7257e15f | C |
| 257 | lessons.md:23 | written stopping rule | NEXT.md quality-read rule; timing unchecked | X |
| 258 | lessons.md:23 | 31 Aug and 2 Sep links | files exist | C |
| 259 | lessons.md:25 | stopped mid-draft, retracted results | d1679987, 10c1dd77 | C |
| 260 | lessons.md:25 | both followed clear instruction | inference | CN |
| 261 | lessons.md:25 | loop page link | file exists | C |
| 262 | lessons.md:27 | planned parts changed most | not traced | X |
| 263 | lessons.md:27 | five-book plan, first draft, first voice rules | not traced | X |
| 264 | lessons.md:27 | lasting parts came from failures | not traced | X |

### workflow/README.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 265 | workflow/README.md:3 | the ten days | index.json | C |
| 266 | workflow/README.md:7 | arcs of 30,000 to 50,000 words | plans/book-01 | C |
| 267 | workflow/README.md:7 | scenes of 600 to 900 words | process.md | C |
| 268 | workflow/README.md:7 | no repeat within four scenes, unless continuous | rule confirmed; exception not found anywhere | CN |
| 269 | workflow/README.md:7 | a dozen times, fifty-odd scenes, six in seven | source says ten, four, chs 44 to 50 | O |
| 270 | workflow/README.md:8 | repair cost a rebuild and two passes | 3ef92e14 | C |
| 271 | workflow/README.md:9 | roughly 2,000-word chapters | voices.md, chapters.json | C |
| 272 | workflow/README.md:13 | David set premise and rules | transcripts | C |
| 273 | workflow/README.md:13 | model did drafting and tooling | transcripts, git | C |
| 274 | workflow/README.md:13 | top notes forbidden to the model | publishing/top-notes/README.md | C |
| 275 | workflow/README.md:13 | everything else machine-written | blurb.md | C |
| 276 | workflow/README.md:14 | the book says so | blurb.md | C |
| 277 | workflow/README.md:15 | catching quality-bar slips | source not found | U |
| 278 | workflow/README.md:15 | checks tightened after misses | git history | C |
| 279 | workflow/README.md:19 | a single interactive session did the drafting | format, not count; see rejected findings | C |
| 280 | workflow/README.md:19 | notes explicit it was not delegated | VOICE.md 133 to 136 | C |
| 281 | workflow/README.md:21 | canon or farming check runs as a subagent | skills | C |
| 282 | workflow/README.md:21 | fan-out then reconcile | language-police SKILL.md | C |
| 283 | workflow/README.md:22 | cheaper and more reliable | pilot-report.md | C |
| 284 | workflow/README.md:23 | workflows above both | transcripts | C |
| 285 | workflow/README.md:23 | used for mechanical sweeps | transcripts | C |

### workflow/claude-md-rules.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 286 | claude-md-rules.md:3 | every session reads CLAUDE.md | docs, git | C |
| 287 | claude-md-rules.md:3 | Claude Code convention | docs memory page | C |
| 288 | claude-md-rules.md:3 | lists files in order | CLAUDE.md items 0 to 7 | C |
| 289 | claude-md-rules.md:5 | exemplars first, not rules | CLAUDE.md item 0 | C |
| 290 | claude-md-rules.md:5 | rules alone satisfy the letter | turn 73 | C |
| 291 | claude-md-rules.md:5 | then rules, tells, premise, canon | CLAUDE.md | C |
| 292 | claude-md-rules.md:5 | start here after a context loss | CLAUDE.md | C |
| 293 | claude-md-rules.md:5 | no memory between conversations | docs | C |
| 294 | claude-md-rules.md:7 | older drafts in git history only | CLAUDE.md 53 to 57 | C |
| 295 | claude-md-rules.md:11 | committed like any asset | git | C |
| 296 | claude-md-rules.md:11 | edits show in git history | git log CLAUDE.md | C |
| 297 | claude-md-rules.md:12 | rule system an artefact of revision | git | C |
| 298 | claude-md-rules.md:13 | sealed answers subagent-only, except on request | CLAUDE.md 112 to 114 | C |
| 299 | claude-md-rules.md:13 | the undecided-mystery failure | CLAUDE.md 100 to 106 | C |
| 300 | claude-md-rules.md:14 | not "write better next time" | CLAUDE.md | C |
| 301 | claude-md-rules.md:17 | voices.md, llm-tells.md, farming.md, VOICE.md | files exist | C |
| 302 | claude-md-rules.md:17 | thin pointer, longer files under it | CLAUDE.md | C |
| 303 | claude-md-rules.md:19 | 2026-08-24 session set the structure | 0c653b33, git | C |

### workflow/voice-and-exemplars.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 304 | voice-and-exemplars.md:3 | rules describe, do not constitute | VOICE.md section 1 | C |
| 305 | voice-and-exemplars.md:3 | read prose before rules | CLAUDE.md item 0 | C |
| 306 | voice-and-exemplars.md:4 | VOICE.md names chapters in order | VOICE.md 12 to 37 | C |
| 307 | voice-and-exemplars.md:5 | six scenes | counted, six files | C |
| 308 | voice-and-exemplars.md:5 | eleven years of shorthand | VOICE.md line 25 | C |
| 309 | voice-and-exemplars.md:9 | rules alone read generic | turn 73 | C |
| 310 | voice-and-exemplars.md:9 | everyone equally clever | llm-tells.md tell 6 | C |
| 311 | voice-and-exemplars.md:9 | locally true, globally useless | VOICE.md, turn 73 | C |
| 312 | voice-and-exemplars.md:11 | exemplars win | VOICE.md 36 to 37 | C |
| 313 | voice-and-exemplars.md:11 | rules annotate exemplars | paraphrase of VOICE.md stance | CN |
| 314 | voice-and-exemplars.md:15 | distance, event-wit, em-dash cap | voices.md 19, item 2, item 6 | C |
| 315 | voice-and-exemplars.md:15 | endings are cuts | voices.md item 7 | C |
| 316 | voice-and-exemplars.md:17 | thirteen binding dialogue rules | voices.md, counted | C |
| 317 | voice-and-exemplars.md:17 | differentiated by content not talk | dialogue-voices.md | C |
| 318 | voice-and-exemplars.md:17 | some do not listen perfectly | voices.md rule 8, llm-tells.md tell 6 | CN |
| 319 | voice-and-exemplars.md:19 | session read NEXT.md and VOICE.md | d1679987 first user turn | C |
| 320 | voice-and-exemplars.md:19 | 2026-08-30 resuming from handoff | index.json start 18:43 | C |
| 321 | voice-and-exemplars.md:19 | transcript link | file exists | C |

### workflow/llm-tells-and-linting.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 322 | llm-tells.md:3 | a fifth of a day early on | 0c653b33 turns 5 to 17 | C |
| 323 | llm-tells.md:3 | over a dozen failure modes | notes/llm-tells.md | C |
| 324 | llm-tells.md:3 | notes/llm-tells.md | file exists | C |
| 325 | llm-tells.md:3 | prose that never rests | llm-tells.md | C |
| 326 | llm-tells.md:3 | a maxim every paragraph | llm-tells.md | C |
| 327 | llm-tells.md:3 | everyone equally articulate | llm-tells.md tell 6 | C |
| 328 | llm-tells.md:7 | 93,000 words, 23 readers | census note in commit cd5fcd2 | C |
| 329 | llm-tells.md:7 | eleven per chapter, four in the seed | voices.md | CN |
| 330 | llm-tells.md:7 | most frequent tell | voices.md census | C |
| 331 | llm-tells.md:7 | one of the more damaging | llm-tells.md rationale | C |
| 332 | llm-tells.md:7 | does the reader's work | llm-tells.md 182 to 185 | C |
| 333 | llm-tells.md:9 | budgets per 1,000 words | voices.md ruled 08-28 | C |
| 334 | llm-tells.md:9 | chapter budget could hide clustering | voices.md | C |
| 335 | llm-tells.md:9 | 3,600 to 2,000 words | voices.md 215 to 227 | C |
| 336 | llm-tells.md:9 | chapters assembled from scenes | voices.md | C |
| 337 | llm-tells.md:13 | tools/lint/prose_lint.py | file exists | C |
| 338 | llm-tells.md:13 | rules.json, regex-catchable | file, tier fields | C |
| 339 | llm-tells.md:13 | just over a hundred entries | 110 | C |
| 340 | llm-tells.md:13 | highest severity fixed mechanically | prose_lint.py exit status | C |
| 341 | llm-tells.md:15 | each rule group a lens | language-police SKILL.md 23 to 31 | C |
| 342 | llm-tells.md:15 | one lightweight call per lens per file | SKILL.md | C |
| 343 | llm-tells.md:15 | handed to a larger judge | SKILL.md aggregation | C |
| 344 | llm-tells.md:17 | regex fast and reliable where expressible | tool design | C |
| 345 | llm-tells.md:17 | only a model can judge earned cleverness | tool design | C |
| 346 | llm-tells.md:17 | not obviously better at recall | pilot-report.md | C |
| 347 | llm-tells.md:21 | new rules enter through David | pilot-report.md, transcripts | C |
| 348 | llm-tells.md:21 | rejected findings logged | 110 counter_examples | C |
| 349 | llm-tells.md:21 | not proposed again | judge prompt | C |
| 350 | llm-tells.md:21 | a record of decisions about this manuscript | rules.json content | C |

### workflow/canon-and-claim-levels.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 351 | canon.md:3 | canon is a separate directory | consistency-backfill SKILL.md | C |
| 352 | canon.md:5 | Established, on-page, cited | consistency-check SKILL.md | C |
| 353 | canon.md:5 | Working, binding until overruled | consistency-backfill SKILL.md | C |
| 354 | canon.md:5 | open questions triaged | deferred-questions.md | C |
| 355 | canon.md:5 | answered, ruled, or deferred with a trigger | canon files | C |
| 356 | canon.md:5 | a triggerless deferral is a defect | canon files | C |
| 357 | canon.md:5 | model proposed, David accepted | transcripts | C |
| 358 | canon.md:9 | the undecided mystery | CLAUDE.md 100 to 106 | C |
| 359 | canon.md:9 | evidence accumulated | CLAUDE.md | C |
| 360 | canon.md:9 | no exceptions | canon files | C |
| 361 | canon.md:11 | sealed answers directory | notes/sealed exists | C |
| 362 | canon.md:11 | written by subagent, never shown unless asked | CLAUDE.md 112 to 114 | C |
| 363 | canon.md:11 | 2026-08-27 sealed-answer check link | transcript exists | C |
| 364 | canon.md:15 | canon not written speculatively | SKILL.md | C |
| 365 | canon.md:15 | consistency-backfill runs after drafting | SKILL.md description | C |
| 366 | canon.md:15 | implications recorded by level | SKILL.md steps 2 and 5 | C |
| 367 | canon.md:15 | smallest binding commitment | SKILL.md step 3 | C |
| 368 | canon.md:15 | conflicts flagged, never silent | SKILL.md steps 3 and 6 | C |
| 369 | canon.md:17 | consistency-check runs the other way | SKILL.md | C |
| 370 | canon.md:17 | core facts first, theme last | theme is softer, not last | CN |
| 371 | canon.md:17 | contradiction and drift | SKILL.md reporting | C |
| 372 | canon.md:17 | neither may weaken canon | SKILL.md canon maintenance | C |
| 373 | canon.md:18 | both flagged, decision is David's | SKILL.md line 37: canon wins | O |

### workflow/next-md-handoff.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 374 | next-md.md:3 | no memory between conversations | docs | C |
| 375 | next-md.md:3 | plans/NEXT.md is the answer | git, file | C |
| 376 | next-md.md:3 | read everything is not workable | file scale | C |
| 377 | next-md.md:7 | five repeating sections | NEXT.md structure | C |
| 378 | next-md.md:9 | the final day's queue | fourth item is a because pass | O |
| 379 | next-md.md:13 | tasks surface more work | git, NEXT.md | C |
| 380 | next-md.md:13 | redrafting flags departures | NEXT.md | C |
| 381 | next-md.md:13 | amendment needs a note left | git | C |
| 382 | next-md.md:15 | edited in place, not append-only | 19 commits | C |
| 383 | next-md.md:15 | canon keeps dated history at the bottom | dated rulings are inline, not at the foot | CN |
| 384 | next-md.md:15 | closed items removed | git log -p | C |
| 385 | next-md.md:17 | last major queue update session | git, 7257e15f | C |
| 386 | next-md.md:17 | 2026-09-02 link | index.json | C |

### workflow/farming-facts-and-author-notes.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 387 | farming.md:3 | facts must be real | notes/farming.md | C |
| 388 | farming.md:3 | magic modifies a real practice | notes/farming.md | C |
| 389 | farming.md:3 | the spell still costs the labour | 0c653b33 turn 158 | C |
| 390 | farming.md:5 | David set the constraint | turn 157 | C |
| 391 | farming.md:5 | a check to pass, not flavour | farming-check skill | C |
| 392 | farming.md:5 | running glossary | farming-glossary.md lines 1 to 8 | C |
| 393 | farming.md:5 | never re-explained, never left unexplained | glossary | C |
| 394 | farming.md:5 | farming-check runs at edit stage | SKILL.md description | C |
| 395 | farming.md:9 | top notes are David's, model may not touch | top-notes/README.md | C |
| 396 | farming.md:9 | agriculture postgraduate persona | notes/author.md 1 to 11 | C |
| 397 | farming.md:9 | the first attempt was boring | notes/author.md | C |
| 398 | farming.md:10 | autobiographical log | notes/author.md line 113 | C |
| 399 | farming.md:11 | accepted drafts read first | notes/author.md | C |
| 400 | farming.md:11 | one digression or two short notes | notes/author.md | C |
| 401 | farming.md:11 | barred from explaining the story | notes/author.md | C |
| 402 | farming.md:12 | only subject is the real fact | notes/author.md | C |
| 403 | farming.md:13 | the map session | c214c046 first turn | C |
| 404 | farming.md:13 | labelled "redrafting scene by scene" | that session built the map | W |
| 405 | farming.md:13 | transcript link | file exists | C |

### workflow/ebook-kindle-proofing.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 406 | ebook.md:3 | David reads before publishing | transcripts | C |
| 407 | ebook.md:3 | a fair amount on a Kindle | 92c486ed | C |
| 408 | ebook.md:3 | needed its own pipeline | tools, git | C |
| 409 | ebook.md:4 | naive approach loses position | kindle_position.py | C |
| 410 | ebook.md:7 | individual scene and chapter files | draft tree | C |
| 411 | ebook.md:7 | collate_book.py | file exists | C |
| 412 | ebook.md:7 | validates numbering | collate_book.py | C |
| 413 | ebook.md:7 | counts body words | collate_book.py | C |
| 414 | ebook.md:7 | writes an index by arc | collate_book.py | C |
| 415 | ebook.md:7 | build_ebook.py makes EPUB and AZW3 | file | C |
| 416 | ebook.md:7 | pandoc and Calibre | build_ebook.py | C |
| 417 | ebook.md:7 | CSS for scene breaks | build_ebook.py | C |
| 418 | ebook.md:9 | AZW3 not MOBI | 92c486ed | C |
| 419 | ebook.md:9 | MOBI pagination freezes | 92c486ed | C |
| 420 | ebook.md:9 | hence Kindle-native from the start | 92c486ed | C |
| 421 | ebook.md:13 | position is a byte offset | kindle_position.py | C |
| 422 | ebook.md:13 | meaningless after an edit | kindle_position.py | C |
| 423 | ebook.md:13 | four-tier fallback | kindle_position.py | C |
| 424 | ebook.md:13 | at least 300 characters | kindle_position.py | C |
| 425 | ebook.md:13 | diff and remap | kindle_position.py | C |
| 426 | ebook.md:13 | fall back to chapter start | kindle_position.py | C |
| 427 | ebook.md:13 | then to book start | kindle_position.py | C |
| 428 | ebook.md:15 | remap before writing | update-kindle.py | C |
| 429 | ebook.md:15 | failure leaves the device working | update-kindle.py | C |
| 430 | ebook.md:15 | update-kindle.py ties it together | file | C |
| 431 | ebook.md:15 | regenerates the pagination index | update-kindle.py | C |
| 432 | ebook.md:15 | stale index causes freezes | 92c486ed | C |
| 433 | ebook.md:15 | macOS leftovers cleaned | update-kindle.py | C |
| 434 | ebook.md:17 | built in a single sitting | 92c486ed | C |
| 435 | ebook.md:17 | grew into the fuller pipeline | git | C |
| 436 | ebook.md:17 | 2026-08-25 session and link | index.json | C |

### workflow/royal-road-publishing.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 437 | rr.md:3 | no public API | site behaviour, tool design | C |
| 438 | rr.md:3 | headless browser scripted with Playwright | only login uses Playwright | O |
| 439 | rr.md:7 | a subcommand per stage | rr.py function defs | C |
| 440 | rr.md:7 | login opens a visible window | cmd_login, PROFILE | C |
| 441 | rr.md:7 | whoami confirms validity | cmd_whoami | C |
| 442 | rr.md:7 | create-fiction posts the submission | cmd_create_fiction | C |
| 443 | rr.md:7 | plan is a dry run | cmd_plan | C |
| 444 | rr.md:7 | go executes | cmd_go | C |
| 445 | rr.md:7 | regroup does three coordinated steps | cmd_regroup docstring | C |
| 446 | rr.md:9 | small markdown subset | rr_convert.py 9 to 13 | C |
| 447 | rr.md:9 | rr_convert.py makes the HTML | chapter_payload in rr.py | C |
| 448 | rr.md:9 | System boxes as styled tables | rr_convert.py 21 to 22, 69 to 71 | C |
| 449 | rr.md:13 | never presses Launch | no such call in rr.py | C |
| 450 | rr.md:13 | commands run after David launched | rr.py, transcripts | C |
| 451 | rr.md:13 | going live sits outside the model | rr.py | C |
| 452 | rr.md:15 | RR's own managed release | cmd_regroup mode and when | C |
| 453 | rr.md:15 | JSON config with metadata | chapters.json, fiction.json | C |
| 454 | rr.md:15 | one chapter a day at a fixed UTC time | commit 614c303, rr-map.json | C |
| 455 | rr.md:15 | the buffer as a recurring topic | NEXT.md, transcripts | C |
| 456 | rr.md:17 | 2026-09-02 buffer session and link | index.json | C |

### workflow/the-commenter.md and workflow/overlap-checking.md

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 457 | commenter.md:1 | local web app at tools/commenter/server.py | file exists | C |
| 458 | commenter.md:1 | built so David could comment properly | transcripts | C |
| 459 | commenter.md:1 | three-pane page | server.py, README.md | C |
| 460 | commenter.md:1 | runs on his own machine | server.py | C |
| 461 | commenter.md:2 | about 160 characters of context | server.py line 21, CONTEXT = 160 | C |
| 462 | commenter.md:2 | exact, moved, fuzzy, orphaned | README.md 27 to 33 | C |
| 463 | commenter.md:2 | short selections relocated wrongly | transcripts, git | C |
| 464 | commenter.md:2 | context was all-or-nothing | server.py history | C |
| 465 | commenter.md:2 | distant edits cost little | _context_score docstring | C |
| 466 | commenter.md:3 | timestamp, body, resolved, anchor | server.py 315 to 318 | C |
| 467 | commenter.md:3 | drafting session checks for new comments | new_comments.py, README.md 45 to 46 | C |
| 468 | overlap.md:5 | runs of eight words | overlap_check.py n = 8 | C |
| 469 | overlap.md:8 | reads from a pinned commit | PIN 44658f1 | C |
| 470 | overlap.md:10 | never loads old prose into context | overlap_check.py docstring | C |
| 471 | overlap.md:11 | CLAUDE.md lists directories never to open | rule is in VOICE.md 3.7 | W |
| 472 | overlap.md:12 | the rule went further than the tool | VOICE.md 154 to 158 | C |
| 473 | overlap.md:13 | drafts deleted once the third draft was accepted | commit 275198e preceded the redraft | W |

### chronicle/*

| # | Page | Claim | Verification | Verdict |
| - | - | - | - | - |
| 474 | chronicle/README.md:15 | dozens of fabricated quotations | actual figure 110 | CN |
| 475 | chronicle/README.md:22 | first forty scenes grouped into chapters | chapters.json, 18 chapters | C |
| 476 | chronicle/2026-08-25.md:9 | census over chapters 1 to 21 | source note says 1 to 23 | W |
| 477 | chronicle/2026-08-26.md:5 | green revolution already established | concept predates, mechanic same day | CN |
| 478 | chronicle/2026-08-27.md | fixing in place would cost more | transcripts | C |
| 479 | chronicle/2026-08-28.md:5 | 206, 110, 38, 58 | commit 135e34d, turn 114 | C |
| 480 | chronicle/2026-08-30.md | act two drafted and pulled | commits 2e285ab, f77e026 | C |
| 481 | chronicle/2026-08-31.md | gated redraft, cleanup, live on RR | commits 275198e, 614c303 | C |
| 482 | chronicle/2026-08-31.md | map addition as a separate session | c214c046 first turn | C |
| 483 | chronicle/2026-09-01.md:4 | schedule ran unattended | no session, no commits that day | C |
| 484 | chronicle/2026-09-02.md | drafted to the end of book one | 7257e15f, NEXT.md | C |

Note on completeness: the claim extraction pass truncated partway through the commenter and overlap-checking claim lists, so a small number of low-risk claims on those two pages and on the chronicle day pages carry no individual verdict row. Everything with a verdict is listed above.

## Rejected findings

Two findings were raised and then refuted on review. They are recorded here so the same objections are not raised again, and written to `build/writing-check/rejected.json` as counter-examples for the next run.

### `howto/setup.md` line 39: "Claude Code can explain what a terminal is, why a command failed, and what a permission prompt means"

Raised as wrong on the grounds that no user turn in the transcripts asks any of these questions. Rejected. The sentence sits in the "If you get stuck" section of a page whose stated audience is "readers who have never opened a terminal". The transcript attribution attaches to the previous sentence's "Ask the model", not to this list, which is a general capability statement addressed to the reader. The page throughout mixes what David did, marked as such, with generic how-to advice that was never transcript-sourced. The separate finding about the previous sentence's attribution clause does stand and is listed as problem 6.

### `workflow/README.md` line 19: "A single interactive session, with David typing prompts and reading replies, did most of the actual drafting"

Raised as overstated on the grounds that drafting happened across many sessions over many days. Rejected. The sentence sits under a heading, "Sessions, subagents, and workflows", that is taxonomising three execution formats, and the following sentence draws the contrast explicitly: "this was deliberately not delegated to subagents, because a persistent session holding the whole conversation in mind produced better prose than a first attempt that split drafting across independent agents." "A single interactive session" is being used adjectivally for the format, not as a count. The proposed fix would have blurred the contrast the paragraph depends on.
