---
name: writing-check
description: Build and run a Workflow that fact-checks and consistency-checks a body of writing (blog posts, documentation, a site, a manuscript's notes) against its primary sources. Use when asked to fact-check, verify claims, check consistency across pages, audit a draft before publication, or "run a review over the writing". Distilled from the fact-check practice in hegel-blog-post and the canon consistency practice in autoroad.
---

# Writing check: fact and consistency verification as a workflow

This skill turns a piece of writing plus its sources into a claim-by-claim verification report and a set of proposed fixes, using the Workflow tool to fan cheap agents over claims and a careful agent over judgements. It is built from two working practices: hegel-blog-post's `fact-check` skill (claim table with receipts, blind checker, primary sources only) and autoroad's `consistency-check` skill and `tools/lint` (priority-ordered ground truth, contradiction/drift/ambiguity, mechanical gates before model judgement, counter-examples to suppress repeat false positives).

## Principles that must survive any adaptation

1. **No receipt, no claim.** Every verdict cites where it was checked: `file:line`, commit SHA, URL, or quoted command output, marked "ran it myself" or "quoted from source". A verdict without a receipt is itself an unverified claim.
2. **Check against primary sources, not summaries.** Research notes, session summaries and earlier reports are drafts of the truth. When the draft was written from a summary, verify the summary too.
3. **The checker is blind.** Verification agents get the text and the sources, never the drafting conversation or earlier reviews. Familiarity with how a claim was written is what makes errors invisible.
4. **Mechanical before judgement.** Anything a script can decide (a number, a quotation, a link target, a date, a name spelling) is decided by a script first. Model verifiers reliably miss greppable defects.
5. **Findings are advisory. Silent edits are never acceptable.** The workflow reports and proposes minimal fixes. Applying them is a separate, visible step, and a finding that would cut a reason, a qualification or an answer is presumptively wrong.
6. **Unverifiable is a verdict.** It leads to a hedge, a cut, or a question for the author. Never to smoothing over.
7. **Suppress repeat false positives with counter-examples, not by loosening the check.** Every rejected finding is logged with why, and the log is fed to the next run.
8. **No findings is a valid result.** Say so plainly rather than inventing nits.

## Claim classes to be paranoid about

Drawn from the errors both projects actually shipped: counts and numbers (miscounted, or the comparison direction reversed); quoted text (must be verbatim against the source at a pinned revision, not lightly paraphrased); absolute statements ("never", "the only", "always"); distributional claims ("most", "almost every") that assert something unmeasured; attributions (who did or said what, which session or day something happened in); dates and ordering; and any claim the writing makes about its own sources ("as the transcript shows").

## Verdicts

`CONFIRMED`, `CONFIRMED-WITH-NUANCE` (true as stated but the source adds a qualification worth carrying), `OVERSTATED` (direction right, strength wrong), `WRONG`, `UNVERIFIABLE` (no source could settle it), `UNCHECKED` (out of scope for this run, say why). Cross-document consistency findings use autoroad's three classes instead: `contradiction` (two passages cannot both be true), `drift` (compatible but one strains the other), `ambiguity` (readable either way; suggest a disambiguation).

## Procedure

### 0. Scope, inline

Before writing the script, list the documents to check and the primary sources they may be checked against, with paths. Decide what is out of scope and say so in the report. Pin revisions (commit SHAs) for any source that changes. Identify which claims can be checked mechanically and write or reuse a small script for them (see step 2). Load the counter-example log from any previous run (`build/writing-check/rejected.json`, or wherever the project keeps it).

### 1. Extract claims (cheap, parallel, one agent per document)

Model: haiku for plain prose, sonnet if the text is dense with technical or numeric claims. Each agent returns a list of checkable claims with: `id`, `quote` (verbatim, at most 300 chars), `location` (file and heading or line), `kind` (number, quotation, attribution, date, absolute, distributional, causal, cross-reference, other), and `check_against` (which source ought to settle it). Instruct: enumerate every checkable claim, do not judge truth, do not skip claims that look obviously right.

Schema:

```js
const CLAIMS = { type: 'object', properties: { claims: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, quote: { type: 'string' }, location: { type: 'string' },
  kind: { type: 'string', enum: ['number','quotation','attribution','date','absolute','distributional','causal','cross-reference','other'] },
  check_against: { type: 'string' } }, required: ['id','quote','location','kind','check_against'] } } }, required: ['claims'] }
```

### 2. Mechanical pre-pass (a script, not an agent)

Run before any model verification and feed its output into step 3 as evidence. Typical checks: every relative link resolves; every number that also appears in a machine-readable source (an index JSON, a git log, a report) matches it; every quotation marked as quoted appears verbatim in its cited source (normalise whitespace and quote characters; classify misses as `FABRICATED`, `ALTERED`, `WRONG_SOURCE` as autoroad's `check_citations.py` does); dates fall inside the range the sources cover; banned terms (spoiler lists, private paths, names not allowed) are absent. Write the script into the project so the next run reuses it.

### 3. Verify claims (blind, parallel, batched)

Model: sonnet. Batch claims by the source they are checked against, so one agent opens each source once. Each agent receives the claims, the source paths, the mechanical pre-pass results relevant to it, and the counter-example log. It receives nothing about how the text was drafted. Instruct: check each claim against the primary source, record a receipt, give one verdict, and for anything other than `CONFIRMED` propose the minimal fix as replacement text. Ask it to be specific about direction and magnitude for numbers and to quote the source for quotations.

Schema:

```js
const VERDICTS = { type: 'object', properties: { results: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, verdict: { type: 'string', enum: ['CONFIRMED','CONFIRMED-WITH-NUANCE','OVERSTATED','WRONG','UNVERIFIABLE','UNCHECKED'] },
  receipt: { type: 'string' }, receipt_kind: { type: 'string', enum: ['ran-it-myself','quoted-from-source','none'] },
  explanation: { type: 'string' }, proposed_fix: { type: 'string' } },
  required: ['id','verdict','receipt','receipt_kind','explanation','proposed_fix'] } } }, required: ['results'] }
```

### 4. Cross-document consistency (parallel, one agent per pair or per topic)

Model: sonnet. Where the writing has several documents that describe the same events, facts or rules, give agents the set of documents grouped by topic and ask for `contradiction`, `drift` and `ambiguity` findings, each quoting both passages with locations and proposing which one to change. Order the checks: hard facts (numbers, names, dates, sequence) first, then attributions, then characterisation of the same event, then tone or register last. Ground truth has a priority order and the agent must be told it (for this site: transcripts and git history, then the parsed index, then session summaries, then the pages themselves).

### 5. Adversarial refutation of negative findings

Every `WRONG`, `OVERSTATED` and `contradiction` finding is handed to a fresh sonnet agent with only the claim, the finding and the sources, prompted to refute the finding. Default to "refuted" if uncertain. A finding survives only if the refuter cannot. This step exists because autoroad's pilot found a 47% false-positive rate among cheap findings, almost all from reading a quote without its neighbouring sentence. Give refuters a wider window than finders.

### 6. Synthesis (one careful agent, opus or the session model)

Produces `fact-check.md` in the project: a "Problems found" section first with the surviving negative findings and full reasoning, then the complete claim table (`# | Claim | Location | Verification | Verdict`), then the consistency findings, then a "Rejected findings" section listing every refuted finding with the reason. It also appends the rejected findings to the counter-example log. It applies no fixes.

### 7. Apply fixes, visibly

A separate agent (or the session) applies the proposed fixes for surviving findings, one document at a time, and records a `Resolution (date)` block at the top of `fact-check.md` saying exactly what changed. `UNVERIFIABLE` claims become hedges, cuts, or questions for the author, listed for them. Then commit the check and the fixes as one commit, and rerun steps 2 and 3 on the changed passages only.

## Workflow script skeleton

```js
export const meta = { name: 'writing-check', description: 'Fact and consistency check of <what> against <sources>',
  phases: [{ title: 'Extract' }, { title: 'Verify' }, { title: 'Consistency' }, { title: 'Refute' }, { title: 'Synthesise' }] }
const DOCS = args.docs            // [{path, sources: [..]}]
const REJECTED = args.rejected    // prior counter-examples, string
const PRE = args.prepass          // output of the mechanical script, string

phase('Extract')
const claims = await parallel(DOCS.map(d => () => agent(extractPrompt(d), { model: 'haiku', effort: 'low', schema: CLAIMS, phase: 'Extract', label: `claims:${d.path}` })))
// group claims by check_against source, in plain code
const batches = groupBySource(claims, DOCS)

phase('Verify')
const verified = await parallel(batches.map(b => () => agent(verifyPrompt(b, PRE, REJECTED), { model: 'sonnet', schema: VERDICTS, phase: 'Verify', label: `verify:${b.source}` })))
const consistency = await parallel(TOPICS.map(t => () => agent(consistencyPrompt(t, DOCS), { model: 'sonnet', schema: CONSISTENCY, phase: 'Consistency' })))

phase('Refute')
const negatives = [...verified.filter(Boolean).flatMap(v => v.results).filter(r => ['WRONG','OVERSTATED'].includes(r.verdict)), ...consistency.filter(Boolean).flatMap(c => c.findings).filter(f => f.klass === 'contradiction')]
const judged = await parallel(negatives.map(n => () => agent(refutePrompt(n), { model: 'sonnet', schema: REFUTE, phase: 'Refute' }).then(r => ({ ...n, refuted: r ? r.refuted : true, why: r ? r.why : 'refuter failed' }))))

phase('Synthesise')
const report = await agent(synthesisPrompt(claims, verified, consistency, judged), { model: 'opus', phase: 'Synthesise' })
return { report, surviving: judged.filter(j => !j.refuted).length, rejected: judged.filter(j => j.refuted).length }
```

Use `pipeline()` rather than the barrier when documents are independent and there is no cross-document stage. Keep the barrier before consistency and synthesis, which genuinely need everything.

## Reporting to the user

Lead with the count of surviving problems and the three most consequential, with the fix applied or proposed for each. Then say what was out of scope, what was unverifiable, and how many findings were refuted, because the refutation rate is the honest measure of how much to trust the rest. Point at `fact-check.md` for the full table. Never describe a check as complete if any document in scope went unchecked.
