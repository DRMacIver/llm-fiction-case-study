"""Render build/redacted/ transcripts into mdBook markdown pages.

Writes:
  site/src/transcripts/<session-id>.md            (split into -part2 etc if >400 turns)
  site/src/transcripts/subagents/<agent-id>.html   standalone static pages, NOT in SUMMARY.md
  site/src/transcripts/README.md                  index table of the 9 sessions
  site/src/SUMMARY.md                              Transcripts section rewritten

Rendering rules (see tools/redact.py docstring for the ⟦...⟧ markers this
consumes):
  - user prompts -> blockquote labelled "David" (session pages) or "User"
    (subagent pages, whose "user" turn is the orchestrating prompt, not the
    human author)
  - assistant prose -> unlabelled paragraphs with a thin left border
  - thinking -> <details><summary>thinking</summary>...</details>
  - each tool_use (+ its tool_result) -> one compact line "🔧 Tool ...";
    a run of more than 5 consecutive tool lines is grouped into one
    <details> block
  - Agent tool_use blocks link to the subagent's standalone HTML page when
    resolvable, with an anchor the subagent page links back to
  - ⟦redacted...⟧ markers -> <span class="redacted">...</span>
  - all transcript text is HTML-escaped; session pages embed this as raw
    HTML inside markdown (mdBook/pulldown-cmark passes raw HTML through
    untouched), and subagent pages embed it directly in a standalone
    <!doctype html> file, so nothing here needs markdown-escaping any more.
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
TITLES_PATH = TRANSCRIPTS_DIR / "titles.json"
PAGE_NOTES_PATH = REPO_ROOT / "tools" / "page-notes.json"

MAX_TURNS_PER_PART = 400
TOOL_GROUP_THRESHOLD = 5

_REDACT_MARKER_RE = re.compile(r"⟦([^⟧]*)⟧")


def esc(text: str) -> str:
    """HTML-escape text and turn the ⟦...⟧ redaction markers this project
    uses into <span class="redacted"> spans."""
    if text is None:
        return ""
    escaped = html.escape(text, quote=False)

    def repl(m: re.Match) -> str:
        inner = m.group(1)
        return f'<span class="redacted">{inner}</span>'

    return _REDACT_MARKER_RE.sub(repl, escaped)


def esc_inline(text: str) -> str:
    """Like esc() but named separately for short inline strings (tool
    summary lines, titles): escape + redaction spans."""
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
            anchor = f'<span id="agent-{sub_id}"></span>'
            line = f'{anchor}🔧 <a href="subagents/{sub_id}.html">{escaped_summary}</a>'
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


def render_turn(turn: dict, subagent_ids: set[str], user_label: str = "User") -> str:
    role = turn.get("role")
    out = []
    blocks = turn.get("blocks", [])
    i = 0
    if role == "user":
        # user turns are usually a single text/command block.
        for b in blocks:
            if b["kind"] == "text":
                quoted = esc(b["text"]).replace("\n", "<br>\n")
                out.append(
                    f'<blockquote><p><strong>{user_label}:</strong><br>\n{quoted}</p></blockquote>\n'
                )
            elif b["kind"] == "command":
                out.append(f"<p><strong>{user_label}:</strong> ran <code>{esc_inline(b.get('name', ''))}</code></p>\n")
        return "\n".join(out)

    # assistant turn: walk blocks, grouping consecutive tool_use/tool_result
    while i < len(blocks):
        b = blocks[i]
        kind = b["kind"]
        if kind == "text":
            paragraphs = "\n".join(
                f"<p>{p.replace(chr(10), '<br>' + chr(10))}</p>"
                for p in esc(b["text"]).split("\n\n")
                if p.strip()
            )
            out.append(f'<div class="assistant-prose">\n{paragraphs}\n</div>\n')
            i += 1
        elif kind == "thinking":
            out.append(
                f"<details><summary>thinking</summary>\n<div>{esc(b['text']).replace(chr(10), '<br>' + chr(10))}</div>\n</details>\n"
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


def render_transcript_body(doc: dict, subagent_ids: set[str], user_label: str = "User") -> str:
    parts = []
    for turn in doc.get("turns", []):
        rendered = render_turn(turn, subagent_ids, user_label)
        if rendered.strip():
            parts.append(rendered)
    return "\n\n".join(parts)


def chunk_turns(turns: list[dict], size: int) -> list[list[dict]]:
    if len(turns) <= size:
        return [turns]
    return [turns[i : i + size] for i in range(0, len(turns), size)]


@dataclass
class RenderedChunk:
    heading: str
    body: str
    part_no: int
    n_parts: int


def render_chunks(doc: dict, title: str, subagent_ids: set[str], user_label: str = "User") -> list[RenderedChunk]:
    turns = doc.get("turns", [])
    chunks = chunk_turns(turns, MAX_TURNS_PER_PART)
    n_parts = len(chunks)
    results = []
    for idx, chunk in enumerate(chunks):
        part_no = idx + 1
        chunk_doc = dict(doc)
        chunk_doc["turns"] = chunk
        body = render_transcript_body(chunk_doc, subagent_ids, user_label)
        heading = title if n_parts == 1 else f"{title} (part {part_no} of {n_parts})"
        results.append(RenderedChunk(heading, body, part_no, n_parts))
    return results


def render_session(
    doc: dict, title: str, subagent_ids: set[str], out_path_stem: Path, note: str | None = None
) -> list[Path]:
    """Render a top-level session as one or more mdBook markdown pages."""
    written = []
    for rc in render_chunks(doc, title, subagent_ids, user_label="David"):
        nav = []
        if rc.n_parts > 1:
            if rc.part_no > 1:
                nav.append(f"[← part {rc.part_no - 1}]({out_path_stem.name}-part{rc.part_no - 1}.md)")
            if rc.part_no < rc.n_parts:
                nav.append(f"[part {rc.part_no + 1} →]({out_path_stem.name}-part{rc.part_no + 1}.md)")
        nav_line = " · ".join(nav)
        page = f"# {rc.heading}\n\n"
        if rc.part_no == 1 and note:
            page += page_note_html(note)
        if nav_line:
            page += nav_line + "\n\n"
        page += rc.body + "\n"
        if nav_line:
            page += "\n" + nav_line + "\n"
        fname = out_path_stem.name if rc.n_parts == 1 else f"{out_path_stem.name}-part{rc.part_no}"
        dest = out_path_stem.parent / f"{fname}.md"
        dest.write_text(page)
        written.append(dest)
    return written


SUBAGENT_STYLE = """<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  max-width:750px;margin:2.5em auto;padding:0 1.2em;line-height:1.6;color:#333;background:#fff;}
h1{font-size:1.4em;}
.subagent-header{color:#666;font-size:.9em;margin-bottom:1.5em;padding-bottom:.6em;border-bottom:1px solid #ddd;}
.subagent-header a{color:#2565ae;}
.redacted{display:inline-block;background:#7a7a7a;color:#fff;border-radius:3px;
  padding:0 .4em;font-size:.85em;font-style:italic;}
details>summary{cursor:pointer;color:#666;}
blockquote{border-left:3px solid #ddd;margin:0 0 1em 0;padding:.2em 0 .2em 1em;color:#444;}
.assistant-prose{border-left:2px solid #ddd;padding-left:.8em;margin:1em 0;}
.nav-links{color:#666;font-size:.9em;margin:1em 0;}
.page-note{background:#f4f0e6;border:1px solid #ddd;border-radius:4px;padding:.6em .9em;
  margin:1em 0;font-size:.92em;color:#555;}
</style>"""


def render_subagent_pages(
    doc: dict,
    title: str,
    agent_id: str,
    parent_session_id: str,
    subagent_ids: set[str],
    note: str | None = None,
) -> list[Path]:
    """Render a subagent transcript as standalone static HTML file(s) under
    site/src/transcripts/subagents/. Not listed in SUMMARY.md."""
    written = []
    chunks = render_chunks(doc, title, subagent_ids, user_label="User")
    n_parts = len(chunks)
    for rc in chunks:
        fname = agent_id if n_parts == 1 else f"{agent_id}-part{rc.part_no}"
        nav = []
        if n_parts > 1:
            if rc.part_no > 1:
                nav.append(f'<a href="{agent_id}-part{rc.part_no - 1}.html">← part {rc.part_no - 1}</a>')
            if rc.part_no < n_parts:
                nav.append(f'<a href="{agent_id}-part{rc.part_no + 1}.html">part {rc.part_no + 1} →</a>')
        nav_html = f'<div class="nav-links">{" · ".join(nav)}</div>' if nav else ""
        header = (
            f'<div class="subagent-header">'
            f'<a href="../{parent_session_id}.html#agent-{agent_id}">← back to session</a>'
            f" &middot; subagent transcript, not indexed</div>"
        )
        note_html = page_note_html(note) if rc.part_no == 1 else ""
        page = (
            "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
            f"<title>{html.escape(rc.heading)}</title>{SUBAGENT_STYLE}</head><body>"
            f"<h1>{html.escape(rc.heading)}</h1>{header}{note_html}{nav_html}{rc.body}{nav_html}"
            "</body></html>\n"
        )
        dest = SUBAGENTS_OUT_DIR / f"{fname}.html"
        dest.write_text(page)
        written.append(dest)
    return written


def format_date(ts: str | None) -> str:
    if not ts:
        return "?"
    return ts.split("T")[0]


def load_titles() -> dict:
    if not TITLES_PATH.is_file():
        return {}
    try:
        return json.loads(TITLES_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def load_page_notes() -> dict:
    """id -> spoiler-free note string, rendered at the top of that session or
    subagent page. See tools/page-notes.json."""
    if not PAGE_NOTES_PATH.is_file():
        return {}
    try:
        raw = json.loads(PAGE_NOTES_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    return {k: v for k, v in raw.items() if not k.startswith("_") and isinstance(v, str)}


def page_note_html(note: str | None) -> str:
    if not note:
        return ""
    return f'<div class="page-note"><em>{esc_inline(note)}</em></div>\n'


def main() -> None:
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    SUBAGENTS_OUT_DIR.mkdir(parents=True, exist_ok=True)

    subagent_ids = load_subagent_ids()
    titles = load_titles()
    page_notes = load_page_notes()

    index_path = REDACTED_DIR / "index.json"
    index = json.loads(index_path.read_text()) if index_path.is_file() else {"sessions": []}

    # Count subagents per parent session first (used in the README table).
    subagent_dir = REDACTED_DIR / "subagents"
    subagent_docs = []
    if subagent_dir.is_dir():
        for p in sorted(subagent_dir.glob("*.json")):
            subagent_docs.append(json.loads(p.read_text()))
    subagent_count_by_session: dict[str, int] = {}
    for d in subagent_docs:
        parent = d.get("parent_session_id")
        if parent:
            subagent_count_by_session[parent] = subagent_count_by_session.get(parent, 0) + 1

    session_rows = []
    for sess_meta in index.get("sessions", []):
        sid = sess_meta["id"]
        src = REDACTED_DIR / f"{sid}.json"
        if not src.is_file():
            continue
        doc = json.loads(src.read_text())
        raw_prompt = sess_meta.get("first_user_prompt", sid) or sid
        fallback_title = truncate(raw_prompt, 70) or sid
        fallback_title = esc_inline(fallback_title)
        title_entry = titles.get(sid, {})
        display_title = esc_inline(title_entry.get("title", "")) if title_entry.get("title") else ""
        stem = TRANSCRIPTS_DIR / sid
        written = render_session(
            doc, display_title or fallback_title, subagent_ids, stem, note=page_notes.get(sid)
        )
        n_turns = len(doc.get("turns", []))
        tool_counts = sess_meta.get("tool_counts", {})
        session_rows.append(
            {
                "id": sid,
                "date": format_date(sess_meta.get("start")),
                "title": display_title,
                "nav_title": display_title or fallback_title,
                "first_prompt": esc_inline(truncate(raw_prompt, 120)),
                "user_turns": sess_meta.get("user_turns", 0),
                "tool_uses": sum(tool_counts.values()),
                "subagent_count": subagent_count_by_session.get(sid, 0),
                "turns": n_turns,
                "link": written[0].name,
            }
        )

    for d in subagent_docs:
        agent_id = d.get("session_id")
        parent_session_id = d.get("parent_session_id", "")
        first_prompt = ""
        for t in d.get("turns", []):
            if t.get("role") == "user":
                for b in t.get("blocks", []):
                    if b.get("kind") == "text":
                        first_prompt = b["text"]
                        break
            if first_prompt:
                break
        title = esc_inline(truncate(first_prompt, 70) or agent_id)
        render_subagent_pages(
            d, title, agent_id, parent_session_id, subagent_ids, note=page_notes.get(agent_id)
        )

    write_readme(session_rows)
    update_summary(session_rows)


def write_readme(session_rows: list[dict]) -> None:
    lines = ["# Transcripts", "", (
        "Full, redacted build transcripts of the Claude Code sessions used to make this "
        "site and the novel's tooling. Spoilers for anything past the published chapters "
        "are replaced with grey ⟦redacted⟧ markers; see [About this site](../about.md)."
    ), ""]
    lines += ["## Sessions", "", "| Date | Title | First prompt | User turns | Tool uses | Subagents | |", "|---|---|---|---|---|---|---|"]
    for row in sorted(session_rows, key=lambda r: r["date"]):
        lines.append(
            f"| {row['date']} | {md_link_text(row['title'])} | {md_link_text(row['first_prompt'])} | "
            f"{row['user_turns']} | {row['tool_uses']} | {row['subagent_count']} | [open]({row['link']}) |"
        )
    lines += ["", (
        "A **session** is one top-level Claude Code conversation, the kind started directly "
        "by David; a **subagent** is a separate conversation a session spawns (via the Agent "
        "or Workflow tools) to do a bounded piece of work and report back. Subagent "
        "transcripts are linked inline from the session that spawned them (look for 🔧 Agent "
        "lines) as standalone pages outside this book's navigation and search index, since "
        "there are far too many of them to list here. Tool calls throughout are shown in a "
        "simplified, one-line form; the contents of files read or written are never shown. "
        "Thinking blocks are collapsed behind a \"thinking\" toggle."
    ), ""]
    (TRANSCRIPTS_DIR / "README.md").write_text("\n".join(lines) + "\n")


def update_summary(session_rows: list[dict]) -> None:
    text = SUMMARY_PATH.read_text()
    marker = "- [Transcripts](transcripts.md)"
    lines = ["- [Transcripts](transcripts/README.md)"]
    for row in sorted(session_rows, key=lambda r: r["date"]):
        lines.append(
            f"  - [{row['date']}: {md_link_text(row['nav_title'])}](transcripts/{row['link']})"
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
