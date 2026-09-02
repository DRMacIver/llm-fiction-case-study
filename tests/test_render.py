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


def test_esc_neutralises_leading_markdown_tokens():
    out = render.esc("# not a heading\n- not a list item\n> not a quote")
    for line in out.split("\n"):
        stripped = line.lstrip(" ")
        assert not stripped.startswith("#")
        assert not stripped.startswith("- ") or "&#8203;" in line
        assert not stripped.startswith(">") or "&#8203;" in line


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


def test_render_turn_user_is_blockquoted():
    turn = {"role": "user", "blocks": [{"kind": "text", "text": "hello there"}]}
    out = render.render_turn(turn, subagent_ids=set())
    assert "**User:**" in out
    assert "> hello there" in out


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
