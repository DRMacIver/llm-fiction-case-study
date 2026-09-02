import json

from tools import render


def test_esc_escapes_html():
    out = render.esc("<script>alert(1)</script> & stuff")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out
    assert "&amp;" in out


def test_esc_renders_redaction_marker_as_span():
    out = render.esc("before ⟦redacted: character⟧ after")
    assert '<span class="redacted">redacted: character</span>' in out
    assert "⟦" not in out and "⟧" not in out


def test_esc_inline_short_form():
    out = render.esc_inline("<b>x</b> ⟦redacted: place⟧")
    assert "&lt;b&gt;" in out
    assert '<span class="redacted">redacted: place</span>' in out


def test_truncate_short_text_untouched():
    assert render.truncate("hello", 100) == "hello"


def test_truncate_long_text_gets_ellipsis():
    out = render.truncate("x" * 200, 50)
    assert len(out) == 50
    assert out.endswith("…")


def test_truncate_collapses_newlines():
    out = render.truncate("line one\nline two", 100)
    assert "\n" not in out


def test_tool_use_summary_bash():
    out = render.tool_use_summary(
        {"tool": "Bash", "command": "git log --oneline", "description": "Show recent commits"}
    )
    assert "Bash: git log --oneline" in out
    assert "Show recent commits" in out


def test_tool_use_summary_edit():
    out = render.tool_use_summary({"tool": "Edit", "file": "draft/book-01/scenes/12-x.md"})
    assert out == "Edit draft/book-01/scenes/12-x.md"


def test_tool_use_summary_agent():
    out = render.tool_use_summary({"tool": "Agent", "description": "Canon lens on scene 23"})
    assert "Agent: Canon lens on scene 23" in out


def test_tool_use_line_links_to_known_subagent():
    block = {"tool": "Agent", "description": "check things", "subagent_id": "abc123"}
    out = render.tool_use_line(block, subagent_ids={"abc123"})
    assert '<a href="subagents/abc123.html">' in out
    assert 'id="agent-abc123"' in out


def test_tool_use_line_no_link_for_unknown_subagent():
    block = {"tool": "Agent", "description": "check things", "subagent_id": "missing"}
    out = render.tool_use_line(block, subagent_ids=set())
    assert "<a href" not in out


def test_render_block_group_groups_long_runs():
    blocks = [{"kind": "tool_use", "tool": "Bash", "command": f"echo {i}"} for i in range(7)]
    out = render.render_block_group(blocks, subagent_ids=set())
    assert "<details>" in out
    assert "7 tool calls" in out


def test_render_block_group_no_grouping_for_short_runs():
    blocks = [{"kind": "tool_use", "tool": "Bash", "command": "echo hi"}]
    out = render.render_block_group(blocks, subagent_ids=set())
    assert "<details>" not in out


def test_render_turn_user_default_label():
    turn = {"role": "user", "blocks": [{"kind": "text", "text": "hello there"}]}
    out = render.render_turn(turn, subagent_ids=set())
    assert "<strong>User:</strong>" in out
    assert "hello there" in out
    assert "<blockquote>" in out


def test_render_turn_user_david_label():
    turn = {"role": "user", "blocks": [{"kind": "text", "text": "hello there"}]}
    out = render.render_turn(turn, subagent_ids=set(), user_label="David")
    assert "<strong>David:</strong>" in out
    assert "<strong>User:</strong>" not in out


def test_render_turn_assistant_prose_has_border_and_no_label():
    turn = {"role": "assistant", "blocks": [{"kind": "text", "text": "some prose"}]}
    out = render.render_turn(turn, subagent_ids=set())
    assert 'class="assistant-prose"' in out
    assert "some prose" in out
    assert "<strong>" not in out


def test_render_turn_assistant_thinking_in_details():
    turn = {
        "role": "assistant",
        "blocks": [{"kind": "thinking", "text": "pondering things"}],
    }
    out = render.render_turn(turn, subagent_ids=set())
    assert "<summary>thinking</summary>" in out
    assert "pondering things" in out


def test_chunk_turns_no_split_under_limit():
    turns = [{"i": i} for i in range(10)]
    chunks = render.chunk_turns(turns, 400)
    assert len(chunks) == 1


def test_chunk_turns_splits_over_limit():
    turns = [{"i": i} for i in range(950)]
    chunks = render.chunk_turns(turns, 400)
    assert len(chunks) == 3
    assert sum(len(c) for c in chunks) == 950


def test_format_date():
    assert render.format_date("2026-08-24T11:52:22.554Z") == "2026-08-24"
    assert render.format_date(None) == "?"


def test_md_link_text_escapes_brackets():
    out = render.md_link_text("Set model to [1mOpus 5[22m")
    assert "[" not in out
    assert "]" not in out


def test_render_session_writes_markdown_page(tmp_path, monkeypatch):
    monkeypatch.setattr(render, "TRANSCRIPTS_DIR", tmp_path)
    doc = {
        "turns": [
            {"role": "user", "blocks": [{"kind": "text", "text": "hi"}]},
            {"role": "assistant", "blocks": [{"kind": "text", "text": "hello back"}]},
        ]
    }
    written = render.render_session(doc, "A Session", set(), tmp_path / "sess1")
    assert len(written) == 1
    text = written[0].read_text()
    assert text.startswith("# A Session")
    assert "<strong>David:</strong>" in text
    assert "hello back" in text
    assert written[0].suffix == ".md"


def test_render_subagent_pages_writes_standalone_html(tmp_path, monkeypatch):
    monkeypatch.setattr(render, "SUBAGENTS_OUT_DIR", tmp_path)
    doc = {
        "turns": [
            {"role": "user", "blocks": [{"kind": "text", "text": "do the thing"}]},
            {"role": "assistant", "blocks": [{"kind": "text", "text": "did it"}]},
        ]
    }
    written = render.render_subagent_pages(doc, "Sub Task", "agent-1", "parent-session", set())
    assert len(written) == 1
    dest = written[0]
    assert dest.suffix == ".html"
    text = dest.read_text()
    assert text.startswith("<!doctype html>")
    assert "<style>" in text
    assert '<a href="../parent-session.html#agent-agent-1">' in text
    assert "subagent transcript, not indexed" in text
    assert "<strong>User:</strong>" in text
    assert "<strong>David:</strong>" not in text
    assert "did it" in text


def test_render_subagent_pages_chunks_long_transcripts(tmp_path, monkeypatch):
    monkeypatch.setattr(render, "SUBAGENTS_OUT_DIR", tmp_path)
    monkeypatch.setattr(render, "MAX_TURNS_PER_PART", 2)
    doc = {
        "turns": [
            {"role": "user", "blocks": [{"kind": "text", "text": f"turn {i}"}]}
            for i in range(5)
        ]
    }
    written = render.render_subagent_pages(doc, "Long", "agent-2", "parent", set())
    assert len(written) > 1
    names = sorted(p.name for p in written)
    assert names[0] == "agent-2-part1.html"


def test_load_titles_missing_file_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(render, "TITLES_PATH", tmp_path / "titles.json")
    assert render.load_titles() == {}


def test_load_titles_reads_json(tmp_path, monkeypatch):
    p = tmp_path / "titles.json"
    p.write_text(json.dumps({"sess1": {"title": "A Title", "blurb": "b"}}))
    monkeypatch.setattr(render, "TITLES_PATH", p)
    assert render.load_titles() == {"sess1": {"title": "A Title", "blurb": "b"}}


def test_write_readme_lists_sessions_only(tmp_path, monkeypatch):
    monkeypatch.setattr(render, "TRANSCRIPTS_DIR", tmp_path)
    rows = [
        {
            "date": "2026-08-24",
            "title": "",
            "nav_title": "First session",
            "first_prompt": "Hello world",
            "user_turns": 10,
            "tool_uses": 20,
            "subagent_count": 3,
            "link": "sess1.md",
        }
    ]
    render.write_readme(rows)
    text = (tmp_path / "README.md").read_text()
    assert "Hello world" in text
    assert "| 10 |" in text
    assert "| 20 |" in text
    assert "| 3 |" in text
    assert "subagent" in text.lower()


def test_update_summary_lists_sessions_only(tmp_path, monkeypatch):
    summary = tmp_path / "SUMMARY.md"
    summary.write_text("# Summary\n\n- [Transcripts](transcripts.md)\n")
    monkeypatch.setattr(render, "SUMMARY_PATH", summary)
    rows = [
        {"date": "2026-08-24", "nav_title": "First session", "link": "sess1.md"},
    ]
    render.update_summary(rows)
    text = summary.read_text()
    assert "[Transcripts](transcripts/README.md)" in text
    assert "First session" in text
    assert "subagents/" not in text
