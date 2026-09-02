# Claude Code transcript format notes

Source: `~/.claude/projects/-Users-drmaciver-Projects-autoroad/`

## Layout

```
<session-id>.jsonl                       main session transcript
<session-id>/
  subagents/
    agent-<id>.jsonl                     a subagent's own transcript (same jsonl shape)
    agent-<id>.meta.json                 {"agentType", "description", "toolUseId", "spawnDepth", "model"?}
    workflows/
      wf_<runid>/
        agent-<id>.jsonl                 agents spawned *by* a workflow run
        agent-<id>.meta.json             {"agentType": "workflow-subagent", "spawnDepth", "model"}
        journal.jsonl                    workflow step-by-step journal (not parsed)
  workflows/
    wf_<runid>.json                      {"runId", "timestamp", "taskId", "script": "<the js source>"}
    scripts/<name>-wf_<runid>.js         script source, used when Workflow tool_use passes `scriptPath`
  tool-results/                          large tool results spilled to disk (not needed; content already inline in most lines)
```

Sessions launched as background *workflows* show up as an `Agent`/`Workflow`-style
`tool_use` in the parent, and their per-phase agents live under
`subagents/workflows/wf_<runid>/`. We treat every file matching
`subagents/**/agent-*.jsonl` as a subagent transcript, keyed by its agent id
(the hex string after `agent-a`... actually the id **includes** the leading
`a`, e.g. `a72df8276a13ec14b` — that's the whole `agentId`).

## JSONL line `type` values seen

`assistant`, `user`, `system`, `attachment`, `mode`, `ai-title`, `atis-latch`,
`last-prompt`, `bridge-session`, `queue-operation`, `permission-mode`,
`agent-name`, `file-history-snapshot`, `file-history-delta`, `frame-link`,
`artifact-comment-monitor`, `artifact-autoreact-ledger`, `cost-state`.

Only `assistant` and `user` carry conversation content. Everything else is
harness/UI bookkeeping and is ignored by the parser.

## `user` lines: two very different shapes

1. **Real input** (human typed, or a subagent's initiating prompt):
   `message.content` is a **plain string**. This is what starts a new
   "user turn" — *except* that the harness itself also injects several
   kinds of its own output as real-input-shaped lines (see "Harness output
   disguised as real input" below), which the parser recognises and routes
   to a `role="system"` turn (or folds into a `command` block) instead of
   an ordinary `text` block, specifically so nothing downstream has to
   guess after the fact which "user" turns are really the human speaking.
   Ordinary sub-cases once those are peeled off:
   - A local slash command run outside the model loop appears as a pair of
     consecutive real-input lines: a `<local-command-caveat>...</local-command-caveat>`
     line (pure harness noise, dropped) followed by a
     `<command-name>/foo</command-name>\n<command-message>...</command-message>\n<command-args>...</command-args>`
     line, which we turn into a `command` block holding `/foo` (plus an
     `output` field if a `<local-command-stdout>` line follows it — see
     below).
   - Otherwise it's ordinary prose -> a `text` block, taken verbatim.
2. **Tool results**: `message.content` is a **list** of `tool_result` (and
   occasionally `tool_reference`, from the `ToolSearch` deferred-tool
   mechanism, which we treat like any other tool call/result) objects. These
   do **not** start a new turn — they are appended as `tool_result` blocks to
   the *current* assistant turn, since they're just the mechanical
   continuation of the tool loop the assistant is running.

## Harness output disguised as real input

Several kinds of harness/system output arrive as a real-input (plain
`message.content` string) `user` line — the *exact same shape* a human
prompt takes — because that's the only channel the harness has for pushing
unsolicited content back into the conversation. None of these were typed by
David, and the parser (`parse_transcript()`'s real-input branch) special-
cases each one so it never becomes an ordinary `text` block on a
`role="user"` turn:

- **`<task-notification>...</task-notification>`**: fired when an async
  `Agent`/`Workflow` tool_use finishes in the background. Carries
  `<task-id>`, `<tool-use-id>`, `<output-file>`, `<status>`, `<summary>`,
  a `<result>` (the subagent/workflow's actual return value — for a large
  workflow this can be tens of thousands of characters of JSON or nested
  markdown), sometimes `<diagnostics>`, `<failures>` and `<usage>`
  (`<subagent_tokens>`/`<tool_uses>`/`<duration_ms>`), and — only for a
  *subagent* that itself has live background children of its own — an
  explanatory `<note>` about renotification. On a subagent whose own parent
  is one of these background tasks, the tag is additionally preceded by an
  all-caps `[SYSTEM NOTIFICATION - NOT USER INPUT]\nThis is an automated
  background-task event, NOT a message from the user...` warning paragraph
  (the harness's own attempt to stop the model misreading it) — detection
  looks for `<task-notification>` *anywhere* in the line, not just at the
  start, so this variant is still caught. The parser keeps only `<task-id>`,
  `<status>` and `<summary>` (as a `system_note` block with
  `event: "task_notification"`); the `<result>`/`<diagnostics>`/`<failures>`/
  `<usage>`/`<note>` payload is dropped — for an `Agent` tool_use the actual
  output is the linked subagent's own transcript page, and for a `Workflow`
  it duplicates journal data that isn't reader-facing anyway.
- **The `/compact` auto-summary**: `message.content` starting with `"This
  session is being continued from a previous conversation..."` is the
  harness's own compaction summary, addressed to the model (it typically
  ends with instructions like "do not acknowledge the summary"). Becomes a
  `system_note` block with `event: "compaction_summary"`; the summary text
  itself is dropped (it's an internal recap, not narrative content).
- **`<local-command-stdout>...</local-command-stdout>`**: the terminal
  output of a local slash command, arriving as its own real-input line
  after the `<command-name>` line for the same command (see above) — e.g.
  `/compact` itself is *also* preceded, a few lines earlier, by a bare
  literal `"/compact"` real-input line (the only slash command observed to
  echo itself this way *in addition to* the `<command-name>`/
  `<local-command-stdout>` pair; the parser drops that literal echo as pure
  duplication). ANSI/SGR escape codes in the stdout (`\x1b[2m...\x1b[22m`,
  e.g. around `/compact`'s "Compacted" message) are stripped. Folded onto
  the preceding `command` block as an `output` field rather than rendered
  as a separate turn; if no `command` block is pending, it becomes a
  standalone `system_note` with `event: "command_output"`.

All of the above render (in `tools/render.py`) as a small, un-attributed
`<p class="system-note">⚙ ...</p>` line — never inside a "David:"/"User:"
blockquote — except the `command` block itself (`ran /compact`), which
*is* attributed, since running the slash command is a real thing the human
did; only its stdout output is harness-authored.

## `assistant` lines: one line per content block, not one per message

A single logical assistant message (one `message.id`, one `requestId`) is
frequently split across **multiple consecutive JSONL lines**, each carrying
`message.content` as a list with exactly one block (`thinking`, then `text`,
then `tool_use`, ...), chained by `parentUuid`. The parser does not rely on
`message.id` grouping; instead it treats *every* `assistant` line and every
`user` line-with-list-content as continuing the current assistant turn, and
only a real-input `user` line starts a fresh turn. This naturally
reassembles the whole ReAct loop (thinking → text → tool_use → tool_result →
... → text) triggered by one human message into a single assistant turn with
many blocks, which is what we want for a narrative "how it was built" log.

## Linking `tool_use` blocks to their subagent/workflow files

- **`Agent` tool_use** (`id`, `input.description`, `input.subagent_type`,
  `input.prompt`, optionally `input.model`): the matching `tool_result`'s
  `toolUseResult` (on the *following* `user` line) carries `agentId` (e.g.
  `"a72df8276a13ec14b"`) when the agent is async (always observed to be the
  case here), plus `resolvedModel` and `description`. That agent id is the
  filename stem of `subagents/agent-<agentId>.jsonl` (and
  `agent-<agentId>.meta.json`, whose `toolUseId` field round-trips back to
  the tool_use's `id` — used as a sanity check / fallback lookup by scanning
  meta files for a matching `toolUseId` when `agentId` isn't present in the
  result).
- **`Workflow` tool_use** (`input.script` full JS source, or
  `input.scriptPath` pointing at a saved script for a resume): the meta
  block is `export const meta = { name: '...', description: '...', phases:
  [...] }` at the top of the script; parsed with a regex (best-effort — the
  script is JS, not JSON). The number of `agent(` calls in the script body
  (regex `\bagent\s*\(`) is used as an approximate "number of subagents this
  workflow spawns" count (an undercount when a phase loops in JS, but a
  reasonable summary). The matching `tool_result`'s `toolUseResult.runId`
  (e.g. `"wf_27ce5549-cc5"`) links to `workflows/wf_<runid>.json` (has the
  final script) and to the directory `subagents/workflows/wf_<runid>/`,
  which holds one `agent-<id>.jsonl` per spawned agent — each is emitted as
  its own subagent transcript, same as top-level ones, with
  `parent_session_id` set to the *main* session id and `workflow_run_id` set.

## `tool_result` simplification

- `is_error` (or a `toolUseResult.error`/non-2xx-shaped result) → status
  `error`, first 200 chars of the error text kept.
- Otherwise status `ok`, plus a computed `size` (`lines`, `chars`) over the
  flattened text content.
- `Bash` results additionally keep the first 3 lines of `stdout` (each
  truncated to 200 chars) — *unless* the paired `tool_use`'s command looks
  like a file-dumping command (`cat`, `head`, `tail`, `sed -n`, `less`,
  `bat`, `more`, or `<` redirection reads), in which case the output is
  suppressed entirely (it's just file contents, and file contents must
  never be duplicated into the parsed log per the task's hard rule).

## File-path relativization

Tool inputs mostly use absolute paths under `/Users/drmaciver/Projects/autoroad`
(the novel repo, `cwd` for almost every line) or occasionally a scratch dir
under `/private/tmp/claude-501/...`. `Read`/`Edit`/`Write`/`NotebookEdit`
paths are relativized against the novel repo root when they fall under it;
left absolute otherwise.

Anything else in raw text (a Bash command, a subagent's own report, ...) can
still contain the absolute repo path or a scratch-dir path spelled out in
full; that's what `tools/redact.py`'s `private`-category path handling is
for. Two truncation points sit upstream of that redaction and both have to
be careful never to cut a sensitive path in half, or a partial fragment
(`.../Projects/autoroa`, `⟦unpublished`) defeats the whole-string match
that would otherwise have redacted/tagged it:

- `parse_transcripts.truncate()` (used for `CMD_TRUNC`/`GENERIC_INPUT_TRUNC`
  etc., *before* redaction ever runs) extends a cut through the end of a
  literal `REPO_ROOT` occurrence it would otherwise land inside.
- `render.truncate()` (used for on-page one-line summaries, *after*
  redaction has already inserted `⟦...⟧` markers) extends a cut through a
  marker's closing `⟧` (or backs up to before the marker if none is found)
  for the same reason.

## Redaction markers: two different meanings, two different labels

`tools/redact.py` inserts `⟦...⟧` markers for two unrelated purposes, and
`tools/render.py` gives them different HTML so a reader can't confuse one
for the other:

- **Hiding spoiler content** (`⟦redacted⟧`, `⟦redacted: <category>⟧`,
  `⟦redacted sentence: <label>⟧`, "private" and "unpublished prose" being
  the only labels ever shown) → a grey `<span class="redacted">` pill: the
  text really is hidden here.
- **Flagging already-visible content as not-yet-published** (a bare
  `⟦unpublished⟧`, appended after an unpublished path or an above-threshold
  scene number that stays fully visible) → a lighter `<span
  class="unpub-tag">` outline badge. This is *not* hiding anything, so it
  must never reuse the "redacted" pill styling (which reads as "this is a
  hidden spoiler").

A marker's content can knock a `**bold**` or `` `code` `` span in
surrounding prose out of balance (one delimiter survives outside the
marker, its partner was inside text that got swapped for the marker) —
`redact.py` runs a final pass after every other redaction step that drops
a lone trailing `**`/backtick left outside any marker, so the page never
shows broken markdown syntax as a side effect of redaction.

Titles/headings/nav-link labels (an mdBook page H1, `SUMMARY.md` nav text,
a subagent page's `<title>`/`<h1>`) never get a marker rendered as real
`<span>` HTML — `render.esc_title()` renders it as plain bracketed text
(`[redacted]`, `[unpublished]`) instead. Two different downstream contexts
would otherwise mangle a real `<span>`: a standalone subagent page's
`<title>` is HTML5 "escapable raw text" (entities decode, but tags are
never parsed, so a literal `<span>` shows up as raw unparsed markup in the
browser tab), and an mdBook heading/nav link is inline markdown that
HTML-escapes whatever text it's given (so a marker already turned into a
real `<span>` gets escaped *again*, showing the tag syntax itself as
visible page text).
