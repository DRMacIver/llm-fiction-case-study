import json

import pytest

from tools import redact


@pytest.fixture()
def spoilers(tmp_path):
    data = {
        "terms": [
            {
                "term": "Halla",
                "variants": ["Halla's", "Halla Dunmore"],
                "category": "character",
                "scope": "book1",
                "why": "test",
            },
            {
                "term": "the Bittle",
                "variants": [],
                "category": "place",
                "scope": "book1",
                "why": "test",
            },
        ],
        "topics": ["Edwin's death"],
        "topic_regexes": [
            {"topic": "Edwin's death", "pattern": r"\bEdwin('s)?\s+(dies|died|death)\b"},
            {"topic": "plague", "pattern": r"\bplague\b"},
        ],
        "unpublished_path_rules": {
            "path_prefixes": ["plans/", "notes/theme.md"],
            "scene_number_threshold": 40,
        },
    }
    p = tmp_path / "spoilers.json"
    p.write_text(json.dumps(data))
    return redact.Spoilers.load(p)


def test_word_boundary_does_not_match_substring(spoilers):
    counts = redact.RedactionCounts()
    text = "Hallam went to the market."  # should NOT match "Halla"
    out = redact.redact_text(text, spoilers, counts)
    assert out == text
    assert counts.redacted_chars == 0


def test_term_is_redacted_with_category_marker(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("Halla walked to the field.", spoilers, counts)
    assert "Halla" not in out
    assert "⟦redacted: character⟧" in out
    assert counts.by_category["character"] == 1


def test_variant_matches_too(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("Halla's pack was heavy.", spoilers, counts)
    assert "Halla's" not in out
    assert "⟦redacted: character⟧" in out


def test_case_insensitive(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("HALLA arrived.", spoilers, counts)
    assert "HALLA" not in out
    assert "⟦redacted: character⟧" in out


def test_multiword_term_matches(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("They went to the Bittle at dawn.", spoilers, counts)
    assert "Bittle" not in out
    assert "⟦redacted: place⟧" in out


def test_sentence_level_topic_redaction(spoilers):
    counts = redact.RedactionCounts()
    text = "The weather was fine. Edwin dies at the end of the book. Peri walked home."
    out = redact.redact_text(text, spoilers, counts)
    assert "dies" not in out
    assert "⟦redacted sentence: Edwin's death⟧" in out
    assert "The weather was fine." in out
    assert "Peri walked home." in out


def test_scene_number_above_threshold_tagged(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("See scene 57 for details.", spoilers, counts)
    assert "scene 57" in out
    assert "⟦unpublished⟧" in out
    assert counts.unpublished_tags == 1


def test_scene_number_at_or_below_threshold_not_tagged(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("See scene 12 for details.", spoilers, counts)
    assert "⟦unpublished⟧" not in out
    assert counts.unpublished_tags == 0


def test_scene_filename_above_threshold_tagged(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text(
        "Edit draft/book-01/scenes/57-the-ending.md now.", spoilers, counts
    )
    assert "57-the-ending.md" in out
    assert "⟦unpublished⟧" in out


def test_unpublished_path_prefix_tagged(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("Read plans/book-05/overview.md carefully.", spoilers, counts)
    assert "plans/book-05/overview.md" in out
    assert "⟦unpublished⟧" in out


def test_density_computed(spoilers):
    counts = redact.RedactionCounts()
    redact.redact_text("Halla walked far.", spoilers, counts)
    assert 0 < counts.density() <= 1


def test_density_zero_for_empty_total():
    counts = redact.RedactionCounts()
    assert counts.density() == 0.0


def test_redact_block_only_touches_configured_fields(spoilers):
    counts = redact.RedactionCounts()
    block = {"kind": "tool_use", "tool": "Bash", "command": "echo Halla", "unrelated_field": "Halla"}
    out = redact.redact_block(block, spoilers, counts)
    assert "Halla" not in out["command"]
    # tool name itself untouched, and fields not in TEXT_BLOCK_FIELDS untouched
    assert out["tool"] == "Bash"
    assert out["unrelated_field"] == "Halla"


def test_redact_transcript_walks_all_turns_and_blocks(spoilers):
    doc = {
        "session_id": "abc",
        "turns": [
            {
                "role": "user",
                "blocks": [{"kind": "text", "text": "Tell me about Halla."}],
            },
            {
                "role": "assistant",
                "blocks": [
                    {"kind": "text", "text": "Halla is a warden."},
                    {"kind": "tool_use", "tool": "Bash", "command": "grep Halla file.md"},
                ],
            },
        ],
    }
    redacted, counts = redact.redact_transcript(doc, spoilers)
    assert redacted["session_id"] == "abc"
    all_text = json.dumps(redacted)
    assert "Halla" not in all_text
    assert counts.by_category["character"] >= 3


def test_never_leaks_the_raw_term_text(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("Halla and Halla's and the Bittle all appear here.", spoilers, counts)
    assert "Halla" not in out
    assert "Bittle" not in out


def test_claude_projects_path_redacted_as_private(spoilers):
    counts = redact.RedactionCounts()
    text = (
        "read the full transcript at: "
        "/Users/drmaciver/.claude/projects/-Users-drmaciver-Projects-autoroad/"
        "0c653b33-1efd-45bb-b7ab-26ed3dca981e.jsonl"
    )
    out = redact.redact_text(text, spoilers, counts)
    assert ".claude" not in out
    assert "0c653b33" not in out
    assert "redacted: private" in out
    assert counts.by_category["private"] >= 1


def test_scratch_tmp_path_redacted_as_private(spoilers):
    counts = redact.RedactionCounts()
    text = "Files under /private/tmp/claude-501/-Users-drmaciver-Projects-autoroad/session/foo.json"
    out = redact.redact_text(text, spoilers, counts)
    assert "claude-501" not in out
    assert "redacted: private" in out


def test_topic_marker_not_corrupted_by_later_term_pass(tmp_path):
    # Regression: a topic-sentence marker's own topic *name* can contain a
    # word that a later term rule also matches (e.g. topic "Edwin's
    # death/mortality" contains the literal text "Edwin's death", which a
    # term rule for "Edwin's death" would otherwise re-match and blank out
    # inside the marker), producing a nested/corrupted marker like
    # "⟦redacted sentence: ⟦redacted: event⟧/mortality⟧" instead of a clean
    # single marker.
    data = {
        "terms": [
            {
                "term": "Edwin's death",
                "variants": ["Edwin's mortality"],
                "category": "event",
                "scope": "ending",
                "why": "test",
            }
        ],
        "topics": ["Edwin's death/mortality"],
        "topic_regexes": [
            {
                "topic": "Edwin's death/mortality",
                "pattern": r"\bEdwin('s)?\s+(dies|died|death|mortality)\b",
            }
        ],
        "unpublished_path_rules": {"path_prefixes": [], "scene_number_threshold": 40},
    }
    p = tmp_path / "spoilers.json"
    p.write_text(json.dumps(data))
    spoilers = redact.Spoilers.load(p)

    counts = redact.RedactionCounts()
    out = redact.redact_text("Edwin's death is near.", spoilers, counts)
    assert out == "⟦redacted sentence: Edwin's death/mortality⟧"
    assert out.count(redact.CHAR_MARK) == 1  # single, non-nested marker


def test_toolu_id_redacted_as_private(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("tool call toolu_01CSjJ5NdHPt86TgeEc8H1hH returned.", spoilers, counts)
    assert "toolu_" not in out
    assert "redacted: private" in out
