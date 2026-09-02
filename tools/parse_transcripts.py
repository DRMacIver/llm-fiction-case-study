"""Parse Claude Code jsonl transcripts of the autoroad novel project into a
simplified, spoiler-safe(ish -- no file contents, no thinking-signature blobs)
JSON form suitable for driving a "how it was built" website.

See tools/FORMAT_NOTES.md for the format this reverse-engineers.

Usage:
    uv run python tools/parse_transcripts.py [--src DIR] [--out DIR]

Defaults: src = ~/.claude/projects/-Users-drmaciver-Projects-autoroad,
          out = <repo>/build/parsed
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Iterator

DEFAULT_SRC = Path.home() / ".claude/projects/-Users-drmaciver-Projects-autoroad"
REPO_ROOT = "/Users/drmaciver/Projects/autoroad"

TOOLS_DIR = Path(__file__).resolve().parent
SPOILERS_PATH = TOOLS_DIR / "spoilers.json"


def _load_premise_cutoff() -> "datetime | None":
    try:
        raw = json.loads(SPOILERS_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    ts = raw.get("premise_revealed_at")
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


PREMISE_CUTOFF = _load_premise_cutoff()


def _parse_ts(ts: str | None) -> "datetime | None":
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def is_pre_cutoff(ts: str | None) -> bool:
    """True if a turn/block timestamp is strictly before the premise-reveal
    cutoff (or the cutoff is unset/unparseable, in which case everything is
    treated as post-cutoff -- i.e. no extra content is kept)."""
    if PREMISE_CUTOFF is None:
        return False
    parsed = _parse_ts(ts)
    return parsed is not None and parsed < PREMISE_CUTOFF


# Bash heredoc payload: `<<'EOF' ... EOF` / `<<-EOF ... EOF` / `<<EOF ... EOF`
# (optionally quoted delimiter). Used only to decide whether a pre-cutoff
# Bash tool_use's full command text is worth keeping as `content` -- a
# heredoc is the one Bash shape whose payload can be many lines of quoted
# file content that `truncate()` would otherwise chop.
_HEREDOC_RE = re.compile(r"<<-?\s*['\"]?\w+['\"]?")

TEXT_TRUNC = 300
CMD_TRUNC = 200
GENERIC_INPUT_TRUNC = 200
BASH_LINE_TRUNC = 200
ERROR_TRUNC = 200

FILE_TOOLS = {"Read", "Edit", "Write", "NotebookEdit"}

# Commands whose stdout is liable to include verbatim file contents (as
# opposed to a status line, a count, a filename list, etc). Deliberately
# broad and denylist-shaped: grep/awk/perl/etc. context lines, git show/diff/
# log -p hunks, and interpreter one-liners that read files can all surface
# quoted story prose or unpublished plot detail just as readily as cat/sed
# can, so their stdout is never previewed either. Includes a "\n" separator
# so a command later in a multi-line `cmd1\ncmd2` Bash invocation is still
# recognised (not just ones at the very start or after |;&).
CAT_LIKE_RE = re.compile(
    r"(^|[|;&\n]\s*)(cat|head|tail|less|more|bat|grep|egrep|fgrep|rg|awk|perl|jq|"
    r"strings|xxd|od|nl|diff|hexdump)\b"
    r"|\bsed\s+(-n\b|-e?\s*'[^']*p)"
    r"|\bgit\s+(show|diff|log\s+(-p|--patch|-u))\b"
    r"|\b(python[0-9.]*|node)\b[^\n]*(-c\b|\.read\(\)|open\()"
    r"|\bfind\b[^\n]*-exec\s+(cat|grep|sed|head|tail)\b"
    r"|<\s*\S+\s*$",
)


# ---------------------------------------------------------------------------
# small helpers


def truncate(s: str, n: int) -> str:
    """Character-truncate to `n` chars.

    This runs *before* tools/redact.py ever sees the text, so there are no
    ⟦...⟧ markers yet to protect -- but a cut can still land partway
    through a literal occurrence of REPO_ROOT (e.g. ".../Projects/autoroa"
    with the trailing "d" chopped off), and a partial match defeats
    redact.py's later whole-string term match for that exact path, leaking
    the local username/machine path into the page unredacted -- often right
    next to an earlier, complete (and therefore correctly redacted) copy of
    the same path in the same command. Extend the cut through the end of
    that occurrence instead.
    """
    s = s if isinstance(s, str) else str(s)
    if len(s) <= n:
        return s
    cut = n
    # str.find's end-of-range argument bounds the whole match, so it can't
    # find an occurrence that starts before `cut` but extends past it --
    # walk occurrences from the start instead, extending `cut` whenever one
    # straddles it.
    pos = 0
    while True:
        idx = s.find(REPO_ROOT, pos)
        if idx == -1 or idx >= cut:
            break
        end = idx + len(REPO_ROOT)
        cut = max(cut, end)
        pos = end
    return s[:cut] + "…"


def relpath(p: str | None) -> str | None:
    if not p:
        return p
    if p.startswith(REPO_ROOT + "/"):
        return p[len(REPO_ROOT) + 1 :]
    if p == REPO_ROOT:
        return "."
    return p


def flatten_text(content: Any) -> str:
    """Best-effort flatten of an Anthropic-style content value (str, or list
    of blocks / dicts) into plain text, for sizing/truncation purposes."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif "text" in item:
                    parts.append(str(item["text"]))
                else:
                    parts.append(json.dumps(item))
        return "\n".join(parts)
    return json.dumps(content)


def read_jsonl(path: Path) -> Iterator[dict]:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


LOCAL_CAVEAT_RE = re.compile(r"^<local-command-caveat>.*</local-command-caveat>$", re.S)
COMMAND_NAME_RE = re.compile(r"^<command-name>(.*?)</command-name>")

# ---------------------------------------------------------------------------
# harness-injected "real input" user lines
#
# The Claude Code harness delivers several kinds of its *own* output to the
# model as a real-input (plain-string) `user` line -- the same shape a human
# prompt takes (see FORMAT_NOTES.md). None of these were typed by the human:
#
#   - <task-notification>: an async Agent/Workflow's completion is pushed
#     back into the conversation this way, often carrying a huge inlined
#     <result>/<diagnostics>/<usage> payload. The *outcome* is what belongs
#     in the "how it was built" narrative -- the payload duplicates the
#     structured tool_use/tool_result plumbing already parsed elsewhere (or,
#     for an Agent, the linked subagent transcript itself) and is dropped
#     rather than dumped as if it were prose the human wrote. When the
#     notification lands on a *subagent* that itself has live background
#     children, the tag is preceded by an explicit "[SYSTEM NOTIFICATION -
#     NOT USER INPUT] ... NOT a message from the user" warning paragraph --
#     detection looks for the tag anywhere in the line, not just at its
#     start, so this variant is still caught.
#   - The /compact auto-summary ("This session is being continued from a
#     previous conversation...") is the harness's own compaction summary,
#     addressed to the model, not authored by the human.
#   - <local-command-stdout>: the terminal output of a local slash command
#     (paired with a preceding <command-name> real-input line -- see
#     COMMAND_NAME_RE above). Attached to that command's block as `output`
#     rather than rendered as its own turn.
#
# All three are turned into `system_note` blocks on a `role="system"` turn
# (or folded into the preceding `command` block) instead of a `text` block
# on an ordinary `role="user"` turn, so the renderer never has to guess
# after the fact which "user" turns are really the human speaking.
TASK_NOTIFICATION_PREFIX = "<task-notification>"
TASK_SUMMARY_RE = re.compile(r"<summary>(.*?)</summary>", re.S)
TASK_STATUS_RE = re.compile(r"<status>(.*?)</status>", re.S)
COMPACTION_SUMMARY_PREFIX = (
    "This session is being continued from a previous conversation"
)
LOCAL_COMMAND_STDOUT_PREFIX = "<local-command-stdout>"
LOCAL_COMMAND_STDOUT_SUFFIX = "</local-command-stdout>"

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


def strip_ansi(s: str | None) -> str | None:
    """Strip terminal ANSI/SGR escape sequences (e.g. the `\\x1b[2m...\\x1b[22m`
    dimming codes around /compact's "Compacted" stdout) so they don't leak
    into the page as literal bracket-and-digit noise. Requires the real ESC
    byte, so it never touches text that merely *contains* a literal
    ``[1m``-shaped substring."""
    if not s:
        return s
    return _ANSI_RE.sub("", s)


# ---------------------------------------------------------------------------
# tool_use simplification


def summarize_tool_use(
    name: str,
    tool_input: dict,
    workflow_scripts: dict[str, Path],
    keep_full_content: bool = False,
) -> dict:
    block: dict[str, Any] = {"kind": "tool_use", "tool": name}

    if name in FILE_TOOLS:
        path = tool_input.get("file_path") or tool_input.get("notebook_path")
        block["file"] = relpath(path)
        if keep_full_content and name == "Write" and tool_input.get("content") is not None:
            block["content"] = tool_input["content"]
        elif keep_full_content and name == "Edit":
            block["content"] = {
                "old_string": tool_input.get("old_string"),
                "new_string": tool_input.get("new_string"),
            }
        return block

    if name == "Bash":
        raw_command = strip_ansi(tool_input.get("command", "")) or ""
        block["command"] = truncate(raw_command, CMD_TRUNC)
        if tool_input.get("description"):
            block["description"] = strip_ansi(tool_input["description"])
        if keep_full_content and _HEREDOC_RE.search(raw_command):
            block["content"] = raw_command
        return block

    if name == "Agent":
        block["description"] = tool_input.get("description")
        block["model"] = tool_input.get("model")
        block["subagent_type"] = tool_input.get("subagent_type")
        block["prompt"] = truncate(tool_input.get("prompt", ""), 300)
        return block

    if name == "Workflow":
        script_text = tool_input.get("script")
        if not script_text and tool_input.get("scriptPath"):
            sp = Path(tool_input["scriptPath"])
            if sp.exists():
                try:
                    script_text = sp.read_text(errors="replace")
                except OSError:
                    script_text = None
        meta_name = meta_desc = None
        agent_calls = None
        if script_text:
            m = re.search(r"name\s*:\s*'([^']*)'", script_text)
            meta_name = m.group(1) if m else None
            m = re.search(r"description\s*:\s*'([^']*)'", script_text)
            meta_desc = m.group(1) if m else None
            agent_calls = len(re.findall(r"\bagent\s*\(", script_text))
        block["workflow_name"] = meta_name
        block["workflow_description"] = meta_desc
        block["agent_call_count"] = agent_calls
        return block

    if name in ("Grep", "Glob"):
        block["pattern"] = tool_input.get("pattern")
        return block

    if name in ("WebFetch",):
        block["url"] = tool_input.get("url")
        return block

    if name in ("WebSearch",):
        block["query"] = tool_input.get("query")
        return block

    block["input"] = truncate(json.dumps(tool_input, default=str), GENERIC_INPUT_TRUNC)
    return block


def summarize_tool_result(
    tool_use_id: str | None,
    content: Any,
    tool_use_result: dict | None,
    tool_use_index: dict[str, dict],
) -> dict:
    block: dict[str, Any] = {"kind": "tool_result"}

    is_error = False
    if isinstance(content, dict) and content.get("is_error"):
        is_error = True
    if isinstance(tool_use_result, dict) and tool_use_result.get("stderr") and tool_use_result.get(
        "interrupted"
    ):
        is_error = True

    text = flatten_text(content)
    block["status"] = "error" if is_error else "ok"
    block["size"] = {"lines": text.count("\n") + (1 if text else 0), "chars": len(text)}

    if is_error:
        block["error"] = truncate(text, ERROR_TRUNC)
        return block

    matched = tool_use_index.get(tool_use_id) if tool_use_id else None
    if matched and matched.get("name") == "Bash":
        command = matched.get("input", {}).get("command", "") or ""
        stdout = None
        if isinstance(tool_use_result, dict):
            stdout = tool_use_result.get("stdout")
        if stdout is None:
            stdout = text
        if not CAT_LIKE_RE.search(command):
            lines = stdout.splitlines()[:3]
            if lines:
                block["stdout_preview"] = [truncate(strip_ansi(l), BASH_LINE_TRUNC) for l in lines]

    return block


# ---------------------------------------------------------------------------
# turn assembly


@dataclass
class Turn:
    role: str
    timestamp: str | None
    blocks: list[dict] = field(default_factory=list)

    def to_json(self) -> dict:
        return {"role": self.role, "timestamp": self.timestamp, "blocks": self.blocks}


@dataclass
class ParsedTranscript:
    session_id: str
    start: str | None = None
    end: str | None = None
    git_branch: str | None = None
    cwd: str | None = None
    turns: list[Turn] = field(default_factory=list)
    agent_links: list[dict] = field(default_factory=list)  # {tool_use_id, agent_id}
    workflow_links: list[dict] = field(default_factory=list)  # {tool_use_id, run_id}

    def to_json(self) -> dict:
        return {
            "session_id": self.session_id,
            "start": self.start,
            "end": self.end,
            "git_branch": self.git_branch,
            "cwd": self.cwd,
            "turns": [t.to_json() for t in self.turns],
        }


def parse_transcript(session_id: str, lines: Iterable[dict]) -> ParsedTranscript:
    result = ParsedTranscript(session_id=session_id)
    tool_use_index: dict[str, dict] = {}  # tool_use_id -> {"name":..., "input":...}
    current: Turn | None = None
    # The most recently emitted `command` block (from a <command-name> real-
    # input line) still waiting to pick up its <local-command-stdout>, if
    # any -- see the harness-injected-real-input-lines note above.
    last_command_block: dict | None = None

    def flush_ts(ts: str | None) -> None:
        if ts is None:
            return
        if result.start is None or ts < result.start:
            result.start = ts
        if result.end is None or ts > result.end:
            result.end = ts

    for d in lines:
        ts = d.get("timestamp")
        flush_ts(ts)
        if result.git_branch is None and d.get("gitBranch"):
            result.git_branch = d["gitBranch"]
        if result.cwd is None and d.get("cwd"):
            result.cwd = d["cwd"]

        t = d.get("type")
        if t == "user":
            msg = d.get("message", {})
            content = msg.get("content")
            if isinstance(content, str):
                stripped = content.strip()
                if LOCAL_CAVEAT_RE.match(stripped):
                    continue  # pure noise
                if stripped == "/compact":
                    # The literal command text David typed. /compact is the
                    # only slash command observed to echo itself this way
                    # *in addition to* the <command-name>/<local-command-
                    # stdout> pair a few lines later (every other slash
                    # command only produces that pair) -- so this line is
                    # pure duplication of the "ran /compact" command block
                    # below, not new information.
                    continue
                if TASK_NOTIFICATION_PREFIX in stripped:
                    # An async Agent/Workflow's completion, pushed back into
                    # the conversation as harness output, not human prose.
                    # For a subagent that itself has live background
                    # children, the harness prefixes the notification with
                    # an explicit "[SYSTEM NOTIFICATION - NOT USER INPUT] ...
                    # NOT a message from the user" warning block before the
                    # <task-notification> tag -- checking a plain prefix
                    # match would leave that variant misattributed to the
                    # (sub)agent's "User:", the very mistake the warning
                    # exists to head off. Keep only enough to say "a
                    # background task finished and here's its one-line
                    # summary" -- the full <result>/<diagnostics>/<usage>
                    # payload is dropped (see module note above).
                    summary_m = TASK_SUMMARY_RE.search(stripped)
                    status_m = TASK_STATUS_RE.search(stripped)
                    current = Turn(role="system", timestamp=ts)
                    current.blocks.append(
                        {
                            "kind": "system_note",
                            "event": "task_notification",
                            "status": status_m.group(1).strip() if status_m else None,
                            "summary": summary_m.group(1).strip() if summary_m else None,
                        }
                    )
                    result.turns.append(current)
                    current = None
                    last_command_block = None
                    continue
                if stripped.startswith(COMPACTION_SUMMARY_PREFIX):
                    # The harness's own /compact continuation summary,
                    # addressed to the model ("do not acknowledge the
                    # summary..."), not authored by David.
                    current = Turn(role="system", timestamp=ts)
                    current.blocks.append(
                        {"kind": "system_note", "event": "compaction_summary"}
                    )
                    result.turns.append(current)
                    current = None
                    last_command_block = None
                    continue
                if stripped.startswith(LOCAL_COMMAND_STDOUT_PREFIX):
                    inner = stripped[len(LOCAL_COMMAND_STDOUT_PREFIX) :]
                    if inner.endswith(LOCAL_COMMAND_STDOUT_SUFFIX):
                        inner = inner[: -len(LOCAL_COMMAND_STDOUT_SUFFIX)]
                    out_text = (strip_ansi(inner) or "").strip()
                    if last_command_block is not None:
                        # Fold the command's own terminal output onto its
                        # `command` block instead of a separate turn, so one
                        # slash-command invocation renders as one event
                        # instead of several disconnected "David:" turns.
                        if out_text:
                            last_command_block["output"] = out_text
                        last_command_block = None
                    elif out_text:
                        current = Turn(role="system", timestamp=ts)
                        current.blocks.append(
                            {
                                "kind": "system_note",
                                "event": "command_output",
                                "summary": out_text,
                            }
                        )
                        result.turns.append(current)
                        current = None
                    continue
                m = COMMAND_NAME_RE.match(stripped)
                if m:
                    current = Turn(role="user", timestamp=ts)
                    block = {"kind": "command", "name": m.group(1)}
                    current.blocks.append(block)
                    result.turns.append(current)
                    current = None  # command turns don't accumulate a reply
                    last_command_block = block
                    continue
                current = Turn(role="user", timestamp=ts)
                current.blocks.append({"kind": "text", "text": strip_ansi(content)})
                result.turns.append(current)
                last_command_block = None
                continue

            # list content -> tool_result(s), appended to the running
            # assistant turn (create one if a session/subagent opens with a
            # tool_result somehow, defensively)
            if current is None or current.role != "assistant":
                current = Turn(role="assistant", timestamp=ts)
                result.turns.append(current)
            if isinstance(content, list):
                tur = d.get("toolUseResult")
                for item in content:
                    if not isinstance(item, dict):
                        continue
                    if item.get("type") == "tool_result":
                        tu_id = item.get("tool_use_id")
                        block = summarize_tool_result(
                            tu_id, item.get("content"), tur, tool_use_index
                        )
                        block["tool"] = (
                            tool_use_index.get(tu_id, {}).get("name") if tu_id else None
                        )
                        if isinstance(tur, dict) and tur.get("agentId"):
                            result.agent_links.append(
                                {"tool_use_id": tu_id, "agent_id": tur["agentId"]}
                            )
                        if isinstance(tur, dict) and tur.get("runId"):
                            result.workflow_links.append(
                                {"tool_use_id": tu_id, "run_id": tur["runId"]}
                            )
                        current.blocks.append(block)
                    elif item.get("type") == "tool_reference":
                        current.blocks.append(
                            {"kind": "tool_result", "status": "ok", "tool": item.get("tool_name")}
                        )
            continue

        if t == "assistant":
            if current is None or current.role != "assistant":
                current = Turn(role="assistant", timestamp=ts)
                result.turns.append(current)
            msg = d.get("message", {})
            for item in msg.get("content", []) or []:
                if not isinstance(item, dict):
                    continue
                itype = item.get("type")
                if itype == "thinking":
                    if item.get("thinking"):
                        current.blocks.append(
                            {"kind": "thinking", "text": item["thinking"]}
                        )
                elif itype == "text":
                    if item.get("text"):
                        current.blocks.append({"kind": "text", "text": item["text"]})
                elif itype == "tool_use":
                    name = item.get("name", "")
                    tool_input = item.get("input", {}) or {}
                    tool_use_index[item.get("id")] = {"name": name, "input": tool_input}
                    block = summarize_tool_use(
                        name, tool_input, {}, keep_full_content=is_pre_cutoff(ts)
                    )
                    block["tool_use_id"] = item.get("id")
                    current.blocks.append(block)
            continue

        # everything else (system, mode, ai-title, ...) is ignored noise.

    return result


# ---------------------------------------------------------------------------
# discovery + linking


def find_agent_files(session_dir: Path) -> dict[str, dict]:
    """Return {agent_id: {"jsonl": Path, "meta": Path|None, "workflow_run_id": str|None}}"""
    out: dict[str, dict] = {}
    subagents_dir = session_dir / "subagents"
    if not subagents_dir.exists():
        return out
    for jsonl_path in subagents_dir.rglob("agent-*.jsonl"):
        stem = jsonl_path.stem  # "agent-a72df8..."
        agent_id = stem[len("agent-") :]
        meta_path = jsonl_path.with_suffix("").with_suffix(".meta.json")
        # jsonl_path.with_suffix("") turns "agent-x.jsonl" -> "agent-x"; add .meta.json
        meta_path = jsonl_path.parent / (stem + ".meta.json")
        workflow_run_id = None
        rel = jsonl_path.relative_to(subagents_dir)
        if len(rel.parts) >= 3 and rel.parts[0] == "workflows":
            workflow_run_id = rel.parts[1]
        out[agent_id] = {
            "jsonl": jsonl_path,
            "meta": meta_path if meta_path.exists() else None,
            "workflow_run_id": workflow_run_id,
        }
    return out


def link_agent_ids_via_meta(
    parsed: ParsedTranscript, agent_files: dict[str, dict]
) -> None:
    """Fallback linking: for tool_use ids that never got an agentId from a
    toolUseResult (e.g. malformed/missing result), scan meta.json files for a
    matching toolUseId."""
    linked_tool_use_ids = {l["tool_use_id"] for l in parsed.agent_links}
    tool_use_ids_needing_link = set()
    for turn in parsed.turns:
        for b in turn.blocks:
            if b.get("kind") == "tool_use" and b.get("tool") == "Agent":
                tuid = b.get("tool_use_id")
                if tuid and tuid not in linked_tool_use_ids:
                    tool_use_ids_needing_link.add(tuid)
    if not tool_use_ids_needing_link:
        return
    for agent_id, info in agent_files.items():
        meta_path = info.get("meta")
        if not meta_path:
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        tuid = meta.get("toolUseId")
        if tuid in tool_use_ids_needing_link:
            parsed.agent_links.append({"tool_use_id": tuid, "agent_id": agent_id})


def annotate_agent_and_workflow_links(parsed: ParsedTranscript) -> None:
    by_tool_use_id = {l["tool_use_id"]: l["agent_id"] for l in parsed.agent_links}
    wf_by_tool_use_id = {l["tool_use_id"]: l["run_id"] for l in parsed.workflow_links}
    for turn in parsed.turns:
        for b in turn.blocks:
            if b.get("kind") != "tool_use":
                continue
            tuid = b.get("tool_use_id")
            if b.get("tool") == "Agent" and tuid in by_tool_use_id:
                b["subagent_id"] = by_tool_use_id[tuid]
            if b.get("tool") == "Workflow" and tuid in wf_by_tool_use_id:
                b["workflow_run_id"] = wf_by_tool_use_id[tuid]


def strip_internal_fields(parsed_json: dict) -> dict:
    for turn in parsed_json["turns"]:
        for b in turn["blocks"]:
            b.pop("tool_use_id", None)
    return parsed_json


# ---------------------------------------------------------------------------
# summary / counts


def summarize_for_index(parsed: ParsedTranscript, has_subagents: bool) -> dict:
    user_turns = 0
    tool_counts: dict[str, int] = {}
    first_prompt = None
    for turn in parsed.turns:
        if turn.role == "user":
            for b in turn.blocks:
                if b.get("kind") == "text":
                    user_turns += 1
                    if first_prompt is None and not b["text"].lstrip().startswith("<local-command"):
                        first_prompt = truncate(b["text"], 300)
        for b in turn.blocks:
            if b.get("kind") == "tool_use":
                tool_counts[b["tool"]] = tool_counts.get(b["tool"], 0) + 1
    return {
        "id": parsed.session_id,
        "start": parsed.start,
        "end": parsed.end,
        "git_branch": parsed.git_branch,
        "user_turns": user_turns,
        "tool_counts": tool_counts,
        "has_subagents": has_subagents,
        "first_user_prompt": first_prompt,
    }


# ---------------------------------------------------------------------------
# top-level driver


def process_session(session_jsonl: Path, out_dir: Path) -> tuple[dict, int, list[str]]:
    """Returns (index_entry, n_subagents_written, failures)."""
    session_id = session_jsonl.stem
    session_dir = session_jsonl.parent / session_id
    failures: list[str] = []

    parsed = parse_transcript(session_id, read_jsonl(session_jsonl))
    agent_files = find_agent_files(session_dir)
    link_agent_ids_via_meta(parsed, agent_files)
    annotate_agent_and_workflow_links(parsed)

    (out_dir / "parsed").mkdir(parents=True, exist_ok=True)
    session_out = strip_internal_fields(parsed.to_json())
    with open(out_dir / "parsed" / f"{session_id}.json", "w") as fh:
        json.dump(session_out, fh, indent=2)

    subagents_out_dir = out_dir / "parsed" / "subagents"
    subagents_out_dir.mkdir(parents=True, exist_ok=True)
    n_written = 0
    for agent_id, info in agent_files.items():
        try:
            sub_parsed = parse_transcript(agent_id, read_jsonl(info["jsonl"]))
        except Exception as exc:  # pragma: no cover - defensive
            failures.append(f"{session_id}/{agent_id}: {exc}")
            continue
        link_agent_ids_via_meta(sub_parsed, {})
        annotate_agent_and_workflow_links(sub_parsed)
        sub_json = strip_internal_fields(sub_parsed.to_json())
        sub_json["parent_session_id"] = session_id
        sub_json["workflow_run_id"] = info.get("workflow_run_id")
        meta = {}
        if info.get("meta"):
            try:
                meta = json.loads(info["meta"].read_text())
            except (OSError, json.JSONDecodeError):
                meta = {}
        sub_json["agent_type"] = meta.get("agentType")
        sub_json["description"] = meta.get("description")
        with open(subagents_out_dir / f"{agent_id}.json", "w") as fh:
            json.dump(sub_json, fh, indent=2)
        n_written += 1

    index_entry = summarize_for_index(parsed, has_subagents=bool(agent_files))
    return index_entry, n_written, failures


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1] / "build")
    args = ap.parse_args()

    session_files = sorted(args.src.glob("*.jsonl"))
    index: list[dict] = []
    total_subagents = 0
    total_turns = 0
    failures: list[str] = []

    for session_jsonl in session_files:
        try:
            entry, n_sub, sess_failures = process_session(session_jsonl, args.out)
        except Exception as exc:  # pragma: no cover - defensive
            failures.append(f"{session_jsonl.name}: {exc}")
            continue
        index.append(entry)
        total_subagents += n_sub
        failures.extend(sess_failures)
        parsed_path = args.out / "parsed" / f"{session_jsonl.stem}.json"
        with open(parsed_path) as fh:
            total_turns += len(json.load(fh)["turns"])

    (args.out / "parsed").mkdir(parents=True, exist_ok=True)
    with open(args.out / "parsed" / "index.json", "w") as fh:
        json.dump({"sessions": index}, fh, indent=2)

    print(f"sessions: {len(index)}")
    print(f"subagents: {total_subagents}")
    print(f"total turns: {total_turns}")
    print(f"failures: {len(failures)}")
    for f in failures:
        print(f"  FAIL: {f}")


if __name__ == "__main__":
    main()
