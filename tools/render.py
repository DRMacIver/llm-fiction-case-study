"""Render build/redacted/ transcripts into mdBook markdown pages.

Writes:
  site/src/transcripts/<session-id>.md            (split into -part2 etc if >400 turns)
  site/src/transcripts/subagents/<agent-id>.md
  site/src/transcripts/README.md                  index table
  site/src/SUMMARY.md                              Transcripts section rewritten

Rendering rules (see tools/redact.py docstring for the ⟦...⟧ markers this
consumes):
  - user prompts -> blockquote with a bold "User" label
  - assistant prose -> plain paragraphs
  - thinking -> <details><summary>thinking</summary>...</details>
  - each tool_use (+ its tool_result) -> one compact line "🔧 Tool ...";
    a run of more than 5 consecutive tool lines is grouped into one
    <details> block
  - Agent tool_use blocks link to the subagent's page when resolvable
  - ⟦redacted...⟧ markers -> <span class="redacted">...</span>
  - all transcript text is HTML-escaped and indent-normalised so it can't
    be misread as markdown (code fences, blockquotes, headings, etc.)
"""
from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REDACTED_DIR = REPO_ROOT / "build" / "redacted"
SITE_SRC = REPO_ROOT / "site" / "src"
TRANSCRIPTS_DIR = SITE_SRC / "transcripts"
SUBAGENTS_OUT_DIR = TRANSCRIPTS_DIR / "subagents"
SUMMARY_PATH = SITE_SRC / "SUMMARY.md"

MAX_TURNS_PER_PART = 400
TOOL_GROUP_THRESHOLD = 5

_REDACT_MARKER_RE = re.compile(r"⟦([^⟧]*)⟧")


def esc(text: str) -> str:
    """HTML-escape text and turn the ⟦...⟧ redaction markers this project
    uses into <span class="redacted"> spans, without letting the escaped
    text be interpreted as markdown by mdBook."""
    if text is None:
        return ""
    escaped = html.escape(text, quote=False)
    # Neutralise leading markdown-significant characters per line (list
    # markers, headings, blockquotes, code fences) after escaping, so raw
    # transcript text can never accidentally produce markdown structure.
    lines = escaped.split("\n")
    safe_lines = []
    for line in lines:
        stripped = line.lstrip(" ")
        indent = line[: len(line) - len(stripped)]
        if stripped[:1] in ("#", ">", "-", "*", "+", "`", "|") or re.match(r"^\d+\.\s", stripped):
            stripped = "&#8203;" + stripped  # zero-width space breaks the markdown token
        safe_lines.append(indent + stripped)
    escaped = "\n".join(safe_lines)

    def repl(m: re.Match) -> str:
        inner = m.group(1)
        return f'<span class="redacted">{inner}</span>'

    return _REDACT_MARKER_RE.sub(repl, escaped)


def esc_inline(text: str) -> str:
    """Like esc() but for short inline strings (tool summary lines): no
    per-line markdown neutralisation needed since these render inside a
    single-line context, just escape + redaction spans."""
    if text is None:
        return ""
    escaped = html.escape(text, quote=False)
    return _REDACT_MARKER_RE.sub(lambda m: f'<span class="redacted">{m.group(1)}</span>', escaped)


def md_link_text(text: str) -> str:
    """Make text safe to sit inside markdown `[...]` link-text syntax: escape
    literal brackets (which would otherwise prematurely close the link, e.g.
    stray ANSI-escape `[1m` sequences surviving into a captured prompt)."""
    return text.replace("[", "&#91;").replace("]", "&#93;")


def truncate(text: str | None, n: int = 100) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    if len(text) > n:
        return text[: n - 1].rstrip() + "…"
    return text


@dataclass
class SubagentIndexEntry:
    agent_id: str
    path: Path


def load_subagent_ids() -> set[str]:
    subdir = REDACTED_DIR / "subagents"
    if not subdir.is_dir():
        return set()
    return {p.stem for p in subdir.glob("*.json")}


def tool_use_summary(block: dict) -> str:
    """Return a raw (un-escaped) one-line summary of a tool_use block. The
    caller is responsible for HTML-escaping the result (via esc_inline)
    exactly once before embedding it in the page."""
    tool = block.get("tool", "?")
    if tool == "Bash":
        cmd = truncate(block.get("command", ""), 90)
        desc = block.get("description")
        if desc:
            return f"Bash: {cmd} ({truncate(desc, 60)})"
        return f"Bash: {cmd}"
    if tool in ("Read", "Write", "Edit", "NotebookEdit"):
        return f"{tool} {block.get('file', '')}"
    if tool == "Agent":
        desc = block.get("description", "subagent")
        return f"Agent: {truncate(desc, 80)}"
    if tool == "Workflow":
        name = block.get("workflow_name", "workflow")
        desc = block.get("workflow_description", "")
        n = block.get("agent_call_count")
        extra = f" ({n} agents)" if n else ""
        return f"Workflow: {name}{extra} — {truncate(desc, 60)}"
    if tool == "WebSearch":
        return f"WebSearch: {truncate(block.get('query', ''), 90)}"
    if tool == "WebFetch":
        return f"WebFetch: {truncate(block.get('url', ''), 90)}"
    if tool == "Skill":
        inp = block.get("input")
        if isinstance(inp, str):
            try:
                inp = json.loads(inp)
            except (json.JSONDecodeError, TypeError):
                inp = {}
        skill = (inp or {}).get("skill", "") if isinstance(inp, dict) else ""
        return f"Skill: {skill}"
    return tool


def tool_use_line(block: dict, subagent_ids: set[str]) -> str:
    escaped_summary = esc_inline(tool_use_summary(block))
    line = f"🔧 {escaped_summary}"
    if block.get("tool") == "Agent":
        sub_id = block.get("subagent_id")
        if sub_id and sub_id in subagent_ids:
            line = f'🔧 <a href="subagents/{sub_id}.html">{escaped_summary}</a>'
    return line


def render_block_group(blocks: list[dict], subagent_ids: set[str]) -> str:
    """Render a maximal run of tool_use/tool_result blocks."""
    lines = []
    for b in blocks:
        if b["kind"] == "tool_use":
            lines.append(tool_use_line(b, subagent_ids))
        elif b["kind"] == "tool_result":
            status = b.get("status", "ok")
            marker = "✅" if status == "ok" else "❌"
            size = b.get("size", {})
            detail = f"{marker} {size.get('lines', '?')} lines, {size.get('chars', '?')} chars"
            preview = b.get("stdout_preview")
            if preview:
                preview_text = esc_inline(" / ".join(preview))
                detail += f" — {preview_text}"
            if b.get("error"):
                detail += f" — {esc_inline(truncate(b['error'], 150))}"
            lines.append(detail)
    if len(lines) > TOOL_GROUP_THRESHOLD:
        body = "\n".join(f"<p>{ln}</p>" for ln in lines)
        return f"<details><summary>{len(lines)} tool calls</summary>\n{body}\n</details>\n"
    return "\n".join(f"<p>{ln}</p>" for ln in lines) + "\n"


def render_turn(turn: dict, subagent_ids: set[str]) -> str:
    role = turn.get("role")
    out = []
    blocks = turn.get("blocks", [])
    i = 0
    if role == "user":
        # user turns are usually a single text/command block; render as
        # a blockquote for every text block present.
        for b in blocks:
            if b["kind"] == "text":
                quoted = "\n".join(f"> {line}" for line in esc(b["text"]).split("\n"))
                out.append(f"**User:**\n>\n{quoted}\n")
            elif b["kind"] == "command":
                out.append(f"**User:** ran `{esc_inline(b.get('name', ''))}`\n")
        return "\n".join(out)

    # assistant turn: walk blocks, grouping consecutive tool_use/tool_result
    while i < len(blocks):
        b = blocks[i]
        kind = b["kind"]
        if kind == "text":
            out.append(esc(b["text"]) + "\n")
            i += 1
        elif kind == "thinking":
            out.append(
                f"<details><summary>thinking</summary>\n\n{esc(b['text'])}\n\n</details>\n"
            )
            i += 1
        elif kind in ("tool_use", "tool_result"):
            j = i
            while j < len(blocks) and blocks[j]["kind"] in ("tool_use", "tool_result"):
                j += 1
            out.append(render_block_group(blocks[i:j], subagent_ids))
            i = j
        else:
            i += 1
    return "\n".join(out)


def render_transcript_body(doc: dict, subagent_ids: set[str]) -> str:
    parts = []
    for turn in doc.get("turns", []):
        rendered = render_turn(turn, subagent_ids)
        if rendered.strip():
            parts.append(rendered)
    return "\n\n".join(parts)


def chunk_turns(turns: list[dict], size: int) -> list[list[dict]]:
    if len(turns) <= size:
        return [turns]
    return [turns[i : i + size] for i in range(0, len(turns), size)]


def render_session(doc: dict, title: str, subagent_ids: set[str], out_path_stem: Path) -> list[Path]:
    turns = doc.get("turns", [])
    chunks = chunk_turns(turns, MAX_TURNS_PER_PART)
    written = []
    n_parts = len(chunks)
    for idx, chunk in enumerate(chunks):
        part_no = idx + 1
        chunk_doc = dict(doc)
        chunk_doc["turns"] = chunk
        body = render_transcript_body(chunk_doc, subagent_ids)
        heading = title if n_parts == 1 else f"{title} (part {part_no} of {n_parts})"
        nav = []
        if n_parts > 1:
            if idx > 0:
                nav.append(f"[← part {part_no - 1}]({out_path_stem.name}-part{part_no - 1}.md)")
            if idx < n_parts - 1:
                nav.append(f"[part {part_no + 1} →]({out_path_stem.name}-part{part_no + 1}.md)")
        nav_line = " · ".join(nav)
        page = f"# {heading}\n\n"
        if nav_line:
            page += nav_line + "\n\n"
        page += body + "\n"
        if nav_line:
            page += "\n" + nav_line + "\n"
        fname = out_path_stem.name if n_parts == 1 else f"{out_path_stem.name}-part{part_no}"
        dest = out_path_stem.parent / f"{fname}.md"
        dest.write_text(page)
        written.append(dest)
    return written


def format_date(ts: str | None) -> str:
    if not ts:
        return "?"
    return ts.split("T")[0]


def main() -> None:
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    SUBAGENTS_OUT_DIR.mkdir(parents=True, exist_ok=True)

    subagent_ids = load_subagent_ids()

    index_path = REDACTED_DIR / "index.json"
    index = json.loads(index_path.read_text()) if index_path.is_file() else {"sessions": []}

    session_rows = []
    for sess_meta in index.get("sessions", []):
        sid = sess_meta["id"]
        src = REDACTED_DIR / f"{sid}.json"
        if not src.is_file():
            continue
        doc = json.loads(src.read_text())
        title = truncate(sess_meta.get("first_user_prompt", sid), 70) or sid
        title = esc_inline(title)
        stem = TRANSCRIPTS_DIR / sid
        written = render_session(doc, title, subagent_ids, stem)
        n_turns = len(doc.get("turns", []))
        session_rows.append(
            {
                "id": sid,
                "date": format_date(sess_meta.get("start")),
                "title": title,
                "turns": n_turns,
                "link": written[0].name,
            }
        )

    subagent_rows = []
    for p in sorted((REDACTED_DIR / "subagents").glob("*.json")) if (REDACTED_DIR / "subagents").is_dir() else []:
        doc = json.loads(p.read_text())
        agent_id = doc.get("session_id", p.stem)
        first_prompt = ""
        for t in doc.get("turns", []):
            if t.get("role") == "user":
                for b in t.get("blocks", []):
                    if b.get("kind") == "text":
                        first_prompt = b["text"]
                        break
            if first_prompt:
                break
        title = esc_inline(truncate(first_prompt, 70) or agent_id)
        stem = SUBAGENTS_OUT_DIR / agent_id
        render_session(doc, title, subagent_ids, stem)
        subagent_rows.append(
            {
                "id": agent_id,
                "date": format_date(doc.get("start")),
                "title": title,
                "turns": len(doc.get("turns", [])),
                "link": f"subagents/{agent_id}.md",
            }
        )

    write_readme(session_rows, subagent_rows)
    update_summary(session_rows, subagent_rows)


def write_readme(session_rows: list[dict], subagent_rows: list[dict]) -> None:
    lines = ["# Transcripts", "", (
        "Full, redacted build transcripts of the Claude Code sessions used to make this "
        "site and the novel's tooling. Spoilers for anything past the published chapters "
        "are replaced with grey ⟦redacted⟧ markers; see [About this site](../about.md)."
    ), ""]
    lines += ["## Sessions", "", "| Date | Title | Turns | |", "|---|---|---|---|"]
    for row in sorted(session_rows, key=lambda r: r["date"]):
        lines.append(
            f"| {row['date']} | {md_link_text(row['title'])} | {row['turns']} | [open]({row['link']}) |"
        )
    lines += ["", f"## Subagents ({len(subagent_rows)})", "", (
        "Subagent transcripts are linked inline from the sessions that spawned them "
        "(look for 🔧 Agent lines); see the full list below."
    ), "", "| Date | Title | Turns | |", "|---|---|---|---|"]
    for row in sorted(subagent_rows, key=lambda r: r["date"]):
        lines.append(
            f"| {row['date']} | {md_link_text(row['title'])} | {row['turns']} | [open]({row['link']}) |"
        )
    (TRANSCRIPTS_DIR / "README.md").write_text("\n".join(lines) + "\n")


def update_summary(session_rows: list[dict], subagent_rows: list[dict]) -> None:
    # mdBook only builds pages reachable from SUMMARY.md, so every subagent
    # page must be listed too (even though the nav itself favours the inline
    # 🔧 Agent links) or its link from a session page would 404.
    text = SUMMARY_PATH.read_text()
    marker = "- [Transcripts](transcripts.md)"
    lines = ["- [Transcripts](transcripts/README.md)"]
    for row in sorted(session_rows, key=lambda r: r["date"]):
        lines.append(
            f"  - [{row['date']}: {md_link_text(row['title'])}](transcripts/{row['link']})"
        )
    lines.append("  - [Subagents](transcripts/README.md#subagents)")
    for row in sorted(subagent_rows, key=lambda r: r["date"]):
        lines.append(
            f"    - [{row['date']}: {md_link_text(row['title'])}](transcripts/{row['link']})"
        )
    replacement = "\n".join(lines)
    if marker in text:
        new_text = text.replace(marker, replacement)
    elif "- [Transcripts](transcripts/README.md)" in text:
        new_text = re.sub(
            r"- \[Transcripts\]\(transcripts/README\.md\)(\n {2,}- .*)*",
            replacement,
            text,
        )
    else:
        new_text = text.rstrip("\n") + "\n" + replacement + "\n"
    SUMMARY_PATH.write_text(new_text)


if __name__ == "__main__":
    main()
