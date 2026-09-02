import json

import pytest

from tools import redact


@pytest.fixture()
def spoilers(tmp_path):
    data = {
        "premise_revealed_at": "2026-08-24T13:11:27Z",
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


def test_term_is_redacted_with_generic_marker(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("Halla walked to the field.", spoilers, counts)
    assert "Halla" not in out
    assert "⟦redacted⟧" in out
    assert counts.by_category["character"] == 1


def test_variant_matches_too(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("Halla's pack was heavy.", spoilers, counts)
    assert "Halla's" not in out
    assert "⟦redacted⟧" in out


def test_case_insensitive(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("HALLA arrived.", spoilers, counts)
    assert "HALLA" not in out
    assert "⟦redacted⟧" in out


def test_multiword_term_matches(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("They went to the Bittle at dawn.", spoilers, counts)
    assert "Bittle" not in out
    assert "⟦redacted⟧" in out


def test_sentence_level_topic_redaction(spoilers):
    counts = redact.RedactionCounts()
    text = "The weather was fine. Edwin dies at the end of the book. Peri walked home."
    out = redact.redact_text(text, spoilers, counts)
    assert "dies" not in out
    assert "⟦redacted sentence⟧" in out
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
    assert out == "⟦redacted sentence⟧"
    assert out.count(redact.CHAR_MARK) == 1  # single, non-nested marker


def test_toolu_id_redacted_as_private(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("tool call toolu_01CSjJ5NdHPt86TgeEc8H1hH returned.", spoilers, counts)
    assert "toolu_" not in out
    assert "redacted: private" in out


# ---------------------------------------------------------------------------
# "leaked-private-path": a term that looks like an absolute path must still
# match even when literal two-character "\n" escape sequences (surviving an
# inner layer of JSON-escaping in embedded subagent output) sit right next
# to it instead of a real newline -- the boundary check must not depend on
# what character precedes the path.


@pytest.fixture()
def path_spoilers(tmp_path):
    data = {
        "terms": [
            {
                "term": "/Users/drmaciver/Projects/autoroad",
                "variants": [],
                "category": "private",
                "scope": "n/a",
                "why": "test",
            }
        ],
        "topics": [],
        "topic_regexes": [],
        "unpublished_path_rules": {"path_prefixes": [], "scene_number_threshold": 40},
    }
    p = tmp_path / "spoilers.json"
    p.write_text(json.dumps(data))
    return redact.Spoilers.load(p)


def test_repo_path_term_matches_after_real_newline(path_spoilers):
    counts = redact.RedactionCounts()
    text = "No change needed.\n\n/Users/drmaciver/Projects/autoroad/chapters/009-fenholt.md\n\nDone."
    out = redact.redact_text(text, path_spoilers, counts)
    assert "/Users/drmaciver" not in out
    assert "⟦redacted⟧/chapters/009-fenholt.md" in out


def test_repo_path_term_matches_after_literal_backslash_n(path_spoilers):
    # Regression: text[i] == "n" (a word char) immediately before the "/"
    # used to defeat the (?<!\w) left-boundary check and let the path leak
    # through unredacted.
    counts = redact.RedactionCounts()
    text = "No change needed.\\n\\n/Users/drmaciver/Projects/autoroad/chapters/009-fenholt.md\\n\\nDone."
    out = redact.redact_text(text, path_spoilers, counts)
    assert "/Users/drmaciver" not in out
    assert "⟦redacted⟧/chapters/009-fenholt.md" in out


# ---------------------------------------------------------------------------
# redaction shouldn't leave a markdown emphasis/code delimiter unpaired.


def test_bold_marker_left_unbalanced_by_sentence_redaction_is_stripped(spoilers):
    counts = redact.RedactionCounts()
    # "ch." reads as a sentence end to the naive splitter, so the closing
    # "**" ends up inside the *next* "sentence" -- which then gets redacted
    # as a topic sentence, leaving a stray opening "**" behind.
    text = "**ch. Edwin dies here** Names the spell and explains what it rests on."
    out = redact.redact_text(text, spoilers, counts)
    assert out == "ch. ⟦redacted sentence⟧"
    assert "**" not in out


def test_lone_backtick_left_unbalanced_by_redaction_is_stripped(spoilers):
    counts = redact.RedactionCounts()
    text = "`Halla, 9 wks/2 ch 90); return run"
    out = redact.redact_text(text, spoilers, counts)
    assert "`" not in out


def test_balanced_bold_outside_redaction_is_left_alone(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("This is **bold** and unrelated.", spoilers, counts)
    assert "**bold**" in out


def test_balanced_code_span_outside_redaction_is_left_alone(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("Run `ls -la` please.", spoilers, counts)
    assert "`ls -la`" in out


def test_fenced_code_block_backticks_are_left_alone(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text("```python\nprint(1)\n```", spoilers, counts)
    assert out.count("```") == 2


# ---------------------------------------------------------------------------
# new block kinds introduced for harness-injected content still get redacted


def test_system_note_summary_field_is_redacted(spoilers):
    counts = redact.RedactionCounts()
    block = {"kind": "system_note", "event": "task_notification", "summary": "About Halla's plan"}
    out = redact.redact_block(block, spoilers, counts)
    assert "Halla" not in out["summary"]


def test_command_output_field_is_redacted(spoilers):
    counts = redact.RedactionCounts()
    block = {"kind": "command", "name": "/compact", "output": "mentions Halla"}
    out = redact.redact_block(block, spoilers, counts)
    assert "Halla" not in out["output"]


# ---------------------------------------------------------------------------
# pre-premise-reveal cutoff: only the private-info pass runs


def _text_block(text):
    return {"kind": "text", "text": text}


def test_pre_cutoff_turn_skips_term_and_topic_redaction(spoilers):
    doc = {
        "turns": [
            {
                "role": "user",
                "timestamp": "2026-08-24T13:00:00Z",  # before cutoff
                "blocks": [_text_block("Halla plans; Edwin died today.")],
            }
        ]
    }
    redacted, counts = redact.redact_transcript(doc, spoilers)
    text = redacted["turns"][0]["blocks"][0]["text"]
    assert text == "Halla plans; Edwin died today."
    assert counts.by_category == {}


def test_pre_cutoff_turn_still_redacts_private_info(spoilers):
    doc = {
        "turns": [
            {
                "role": "user",
                "timestamp": "2026-08-24T13:00:00Z",  # before cutoff
                "blocks": [
                    _text_block(
                        "see /Users/drmaciver/.claude/projects/foo/bar.jsonl for details"
                    )
                ],
            }
        ]
    }
    redacted, counts = redact.redact_transcript(doc, spoilers)
    text = redacted["turns"][0]["blocks"][0]["text"]
    assert "/Users/drmaciver/.claude" not in text
    assert "⟦redacted: private⟧" in text


def test_post_cutoff_turn_gets_full_redaction(spoilers):
    doc = {
        "turns": [
            {
                "role": "user",
                "timestamp": "2026-08-24T14:00:00Z",  # after cutoff
                "blocks": [_text_block("Halla plans something.")],
            }
        ]
    }
    redacted, counts = redact.redact_transcript(doc, spoilers)
    text = redacted["turns"][0]["blocks"][0]["text"]
    assert "Halla" not in text
    assert counts.by_category.get("character") == 1


def test_subagent_transcript_uses_its_own_first_timestamp_for_every_turn(spoilers):
    # Subagent's own first timestamp is before the cutoff, so even a later
    # turn inside it (which individually looks post-cutoff) stays exempt
    # from term/topic redaction.
    doc = {
        "start": "2026-08-24T13:05:00Z",
        "turns": [
            {"role": "user", "timestamp": "2026-08-24T13:05:00Z", "blocks": [_text_block("intro")]},
            {
                "role": "assistant",
                "timestamp": "2026-08-24T14:00:00Z",  # would be post-cutoff standalone
                "blocks": [_text_block("Halla walked on.")],
            },
        ],
    }
    redacted, counts = redact.redact_transcript(doc, spoilers, is_subagent=True)
    text = redacted["turns"][1]["blocks"][0]["text"]
    assert text == "Halla walked on."
    assert counts.by_category == {}


def test_subagent_transcript_starting_after_cutoff_gets_full_redaction(spoilers):
    doc = {
        "start": "2026-08-24T14:00:00Z",
        "turns": [
            {"role": "user", "timestamp": "2026-08-24T14:00:00Z", "blocks": [_text_block("Halla walked on.")]},
        ],
    }
    redacted, counts = redact.redact_transcript(doc, spoilers, is_subagent=True)
    text = redacted["turns"][0]["blocks"][0]["text"]
    assert "Halla" not in text


# ---------------------------------------------------------------------------
# "meta" source profile: anonymisation map, broad private-path redaction,
# and disabling scene-number/unpublished-path tagging + the premise cutoff.


def test_anonymize_patterns_replace_longest_match_first():
    patterns = redact.build_anonymize_patterns(
        ["hegel-blog-posts", "hegel-blog-post", "hegel-skill", "hegelator", "hegel"]
    )
    counts = redact.RedactionCounts()
    out = redact._anonymize(
        "Check hegel-blog-post and hegel-skill and hegelator and bare Hegel.",
        patterns,
        "«OTHER-PROJECT»",
        counts,
    )
    assert out == (
        "Check «OTHER-PROJECT» and «OTHER-PROJECT» and «OTHER-PROJECT» and bare «OTHER-PROJECT»."
    )
    assert counts.by_category["anonymized"] == 4


def test_anonymize_does_not_touch_unrelated_words():
    patterns = redact.build_anonymize_patterns(["hegel"])
    counts = redact.RedactionCounts()
    out = redact._anonymize("Hegelianism is unrelated.", patterns, "«OTHER-PROJECT»", counts)
    assert out == "Hegelianism is unrelated."
    assert counts.by_category == {}


def test_redact_text_applies_anonymize_map_before_other_passes(spoilers):
    patterns = redact.build_anonymize_patterns(["hegel-blog-post"])
    counts = redact.RedactionCounts()
    out = redact.redact_text(
        "See /Users/drmaciver/Projects/hegel-blog-post for details.",
        spoilers,
        counts,
        anonymize_patterns=patterns,
        anonymize_placeholder="«OTHER-PROJECT»",
        broad_private_paths=True,
    )
    assert "hegel-blog-post" not in out
    assert "/Users/" not in out
    assert "⟦redacted: private⟧" in out


def test_broad_private_paths_redacts_any_users_path(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text(
        "cd /Users/drmaciver/Projects/some-other-repo && ls",
        spoilers,
        counts,
        broad_private_paths=True,
    )
    assert "/Users/" not in out
    assert "⟦redacted: private⟧" in out


def test_narrow_private_paths_leave_other_users_paths_alone_by_default(spoilers):
    # The "full" (autoroad) profile's default private-path regex only
    # covers Claude Code project storage / the scratch dir, not an
    # arbitrary "/Users/..." path -- unlike the "meta" profile above.
    counts = redact.RedactionCounts()
    out = redact.redact_text(
        "cd /Users/drmaciver/Projects/some-other-repo && ls",
        spoilers,
        counts,
    )
    assert "/Users/drmaciver/Projects/some-other-repo" in out


def test_enable_paths_and_scenes_false_skips_scene_and_unpublished_tagging(path_spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text(
        "See scene 57 and plans/book-05/overview.md for details.",
        path_spoilers,
        counts,
        enable_paths_and_scenes=False,
    )
    assert "unpublished" not in out
    assert "scene 57" in out
    assert "plans/book-05/overview.md" in out


def test_meta_profile_disables_premise_cutoff_in_redact_transcript(spoilers):
    # Even a turn timestamped well before premise_revealed_at gets full
    # (term/topic) redaction when premise_cutoff_enabled=False.
    doc = {
        "turns": [
            {
                "role": "user",
                "timestamp": "2020-01-01T00:00:00Z",
                "blocks": [_text_block("Halla walked on.")],
            }
        ]
    }
    redacted, counts = redact.redact_transcript(doc, spoilers, premise_cutoff_enabled=False)
    text = redacted["turns"][0]["blocks"][0]["text"]
    assert "Halla" not in text
    assert counts.by_category.get("character") == 1


def test_literal_marker_brackets_in_source_are_not_protected(spoilers):
    # Regression: a transcript quoting an old marker label like
    # "⟦redacted sentence: Edwin's death⟧" must not smuggle the label through.
    counts = redact.RedactionCounts()
    out = redact.redact_text("sed s/⟦redacted sentence: Edwin's death⟧/x/", spoilers, counts)
    assert "Edwin's death" not in out
    assert "⟦redacted sentence⟧" in out
