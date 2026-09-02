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
   "user turn". Two sub-cases:
   - A local slash command run outside the model loop appears as a pair of
     consecutive real-input lines: a `<local-command-caveat>...</local-command-caveat>`
     line (pure harness noise, dropped) followed by a
     `<command-name>/foo</command-name>\n<command-message>...</command-message>\n<command-args>...</command-args>`
     line, which we turn into a `command` block holding just `/foo`.
   - Otherwise it's ordinary prose -> a `text` block, taken verbatim.
2. **Tool results**: `message.content` is a **list** of `tool_result` (and
   occasionally `tool_reference`, from the `ToolSearch` deferred-tool
   mechanism, which we treat like any other tool call/result) objects. These
   do **not** start a new turn — they are appended as `tool_result` blocks to
   the *current* assistant turn, since they're just the mechanical
   continuation of the tool loop the assistant is running.

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
