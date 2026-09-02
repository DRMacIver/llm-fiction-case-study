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


def test_esc_gives_bare_unpublished_marker_its_own_tag_class():
    # "unpublished" isn't hiding anything (the path/scene number it's
    # attached to stays fully visible), so it must not look like the
    # "redacted" pill that stands in for genuinely hidden text.
    out = render.esc("plans/book-01/overview.md ⟦unpublished⟧")
    assert '<span class="unpub-tag">unpublished</span>' in out
    assert '<span class="redacted">unpublished</span>' not in out


def test_esc_inserts_separator_between_adjacent_redaction_spans():
    out = render.esc("⟦redacted sentence: unpublished prose⟧⟦redacted: character⟧ charm")
    assert "</span> <span" in out
    assert "</span><span" not in out


def test_esc_title_never_emits_real_html_markup():
    out = render.esc_title("Repo: ⟦redacted: private⟧. ⟦redacted sentence: unpublished prose⟧ The plan")
    assert "<span" not in out
    assert "[redacted]" in out


def test_esc_title_labels_unpublished_marker_distinctly():
    out = render.esc_title("chapters/57-x.md ⟦unpublished⟧")
    assert "[unpublished]" in out


def test_esc_title_escapes_raw_html_once():
    out = render.esc_title("<script>alert(1)</script>")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out
    assert "&amp;lt;" not in out  # never double-escaped


def test_render_markdown_bullet_list():
    out = render.render_markdown("- one\n- two\n- three")
    assert "<ul>" in out
    assert "<li>one</li>" in out
    assert "<li>two</li>" in out


def test_render_markdown_bold():
    out = render.render_markdown("this is **bold** text")
    assert "<strong>bold</strong>" in out


def test_render_markdown_fenced_code_block():
    out = render.render_markdown("some code:\n\n```python\nprint(1)\n```")
    assert "<pre>" in out
    assert "<code" in out
    assert "print(1)" in out


def test_render_markdown_table():
    out = render.render_markdown("| a | b |\n|---|---|\n| 1 | 2 |")
    assert "<table>" in out
    assert "<td>1</td>" in out
    assert '<div class="table-wrap">' in out


def test_render_markdown_redaction_marker_inside_bold():
    out = render.render_markdown("**⟦redacted: character⟧**")
    assert '<span class="redacted">redacted: character</span>' in out
    assert "⟦" not in out and "⟧" not in out
    assert "<strong>" in out


def test_render_markdown_escapes_raw_html_in_source():
    out = render.render_markdown("before <script>alert(1)</script> after")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_truncate_short_text_untouched():
    assert render.truncate("hello", 100) == "hello"


def test_truncate_long_text_gets_ellipsis():
    out = render.truncate("x" * 200, 50)
    assert len(out) == 50
    assert out.endswith("…")


def test_truncate_never_cuts_inside_a_redaction_marker():
    # A naive character-cut here would land inside "⟦unpublished⟧",
    # producing a dangling "⟦unpublished" that esc()/esc_inline() can't
    # recognise as a marker (no closing ⟧) and so leaks raw bracket text.
    text = "cat draft/book-01/scenes/41-calm-hands.md ⟦unpublished⟧ <<'EOF'"
    n = text.index("⟦") + 6  # lands mid-marker
    out = render.truncate(text, n)
    assert "⟦unpublished" not in out or "⟦unpublished⟧" in out
    assert render.esc_inline(out).count("⟦") == 0


def test_truncate_extends_through_marker_close_when_cut_lands_inside_it():
    text = "prefix " + "x" * 5 + "⟦unpublished⟧" + " suffix text that is not shown"
    out = render.truncate(text, len("prefix ") + 5 + 3)  # cut a few chars into the marker
    assert out.startswith("prefix xxxxx⟦unpublished⟧")
    assert out.endswith("…")


def test_truncate_backs_up_before_marker_when_no_closing_bracket_present():
    text = "prefix " + "x" * 5 + "⟦unpublished" + "y" * 50  # malformed: no closing ⟧ anywhere
    out = render.truncate(text, len("prefix ") + 5 + 3)
    assert "⟦" not in out
    assert out == "prefix xxxxx…"


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


def test_tool_use_summary_falls_back_to_input_for_unhandled_tools():
    out = render.tool_use_summary({"tool": "ToolSearch", "input": '{"query": "notebook"}'})
    assert out.startswith("ToolSearch (")
    assert "notebook" in out


def test_tool_use_summary_bare_name_when_no_input():
    out = render.tool_use_summary({"tool": "SomeWeirdTool"})
    assert out == "SomeWeirdTool"


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


def test_render_turn_system_note_never_attributed_to_david():
    turn = {
        "role": "system",
        "blocks": [
            {
                "kind": "system_note",
                "event": "task_notification",
                "summary": 'Agent "Design continent geography" finished',
            }
        ],
    }
    out = render.render_turn(turn, subagent_ids=set(), user_label="David")
    assert "David" not in out
    assert "<blockquote>" not in out
    assert 'class="system-note"' in out
    assert "Design continent geography" in out
    assert "background task finished" in out


def test_render_turn_compaction_summary_note():
    turn = {"role": "system", "blocks": [{"kind": "system_note", "event": "compaction_summary"}]}
    out = render.render_turn(turn, subagent_ids=set(), user_label="David")
    assert "David" not in out
    assert "context compacted" in out


def test_render_turn_command_with_output_shows_system_note_not_david_prose():
    turn = {
        "role": "user",
        "blocks": [{"kind": "command", "name": "/compact", "output": "Compacted"}],
    }
    out = render.render_turn(turn, subagent_ids=set(), user_label="David")
    assert "<strong>David:</strong> ran <code>/compact</code>" in out
    assert 'class="system-note"' in out
    assert "Compacted" in out
    # the output line itself isn't inside the "David:" paragraph
    assert out.count("<strong>David:</strong>") == 1


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


def test_render_transcript_body_inserts_date_markers_on_date_change():
    doc = {
        "turns": [
            {
                "role": "user",
                "timestamp": "2026-08-24T10:00:00.000Z",
                "blocks": [{"kind": "text", "text": "day one"}],
            },
            {
                "role": "assistant",
                "timestamp": "2026-08-24T10:05:00.000Z",
                "blocks": [{"kind": "text", "text": "still day one"}],
            },
            {
                "role": "user",
                "timestamp": "2026-08-25T09:00:00.000Z",
                "blocks": [{"kind": "text", "text": "day two"}],
            },
        ]
    }
    out = render.render_transcript_body(doc, subagent_ids=set())
    assert out.count('class="date-marker"') == 2
    assert "2026-08-24" in out
    assert "2026-08-25" in out
    assert out.index("2026-08-24") < out.index("day one") < out.index("2026-08-25") < out.index("day two")


def test_render_subagent_pages_title_and_h1_not_double_escaped_when_redacted(tmp_path, monkeypatch):
    # Regression: a subagent's title, built via esc_title() in main() and
    # previously re-escaped with html.escape() inside render_subagent_pages,
    # must show up as clean readable text in both <title> and <h1>, never
    # as literal "<span..." tag syntax.
    monkeypatch.setattr(render, "SUBAGENTS_OUT_DIR", tmp_path)
    doc = {"turns": [{"role": "user", "blocks": [{"kind": "text", "text": "do it"}]}]}
    title = render.esc_title("Repo: ⟦redacted: private⟧ plan")
    written = render.render_subagent_pages(doc, title, "agent-9", "parent", set())
    text = written[0].read_text()
    assert "<span" not in text
    assert "&lt;span" not in text
    assert "[redacted]" in text


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


# ---------------------------------------------------------------------------
# pre-cutoff Write/Edit/Bash-heredoc content rendering


def test_render_tool_use_content_returns_none_without_content_field():
    block = {"kind": "tool_use", "tool": "Write", "file": "samples/x.md"}
    assert render.render_tool_use_content(block) is None


def test_render_tool_use_content_write_markdown_file():
    block = {
        "kind": "tool_use",
        "tool": "Write",
        "file": "samples/x.md",
        "content": "# Heading\n\nSome **bold** text.",
    }
    html = render.render_tool_use_content(block)
    assert "<details>" in html
    assert "contents of samples/x.md" in html
    assert "<h1>Heading</h1>" in html
    assert "<strong>bold</strong>" in html


def test_render_tool_use_content_write_non_markdown_uses_pre():
    block = {
        "kind": "tool_use",
        "tool": "Write",
        "file": "scripts/x.py",
        "content": "print('<hi>')",
    }
    html = render.render_tool_use_content(block)
    assert "<pre>" in html
    assert "&lt;hi&gt;" in html


def test_render_tool_use_content_edit_shows_old_and_new():
    block = {
        "kind": "tool_use",
        "tool": "Edit",
        "file": "samples/x.md",
        "content": {"old_string": "before text", "new_string": "after text"},
    }
    html = render.render_tool_use_content(block)
    assert "before text" in html
    assert "after text" in html


def test_render_tool_use_content_bash_heredoc_uses_pre():
    block = {
        "kind": "tool_use",
        "tool": "Bash",
        "content": "cat <<'EOF' > f.md\nsome content\nEOF",
    }
    html = render.render_tool_use_content(block)
    assert "<pre>" in html
    assert "some content" in html


def test_render_block_group_includes_content_details_for_pre_cutoff_write():
    blocks = [
        {
            "kind": "tool_use",
            "tool": "Write",
            "file": "samples/x.md",
            "content": "full early sample prose",
        },
    ]
    html = render.render_block_group(blocks, set())
    assert "full early sample prose" in html
    assert "<details><summary>contents of samples/x.md</summary>" in html


def test_render_block_group_no_content_details_when_no_content_field():
    blocks = [
        {"kind": "tool_use", "tool": "Write", "file": "draft/book-01/scenes/01-x.md"},
    ]
    html = render.render_block_group(blocks, set())
    assert "contents of" not in html
