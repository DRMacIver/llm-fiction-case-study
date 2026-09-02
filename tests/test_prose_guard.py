import json

import pytest

from tools import prose_index, redact


@pytest.fixture()
def spoilers(tmp_path):
    data = {
        "terms": [],
        "topics": [],
        "topic_regexes": [],
        "unpublished_path_rules": {"path_prefixes": [], "scene_number_threshold": 40},
    }
    p = tmp_path / "spoilers.json"
    p.write_text(json.dumps(data))
    return redact.Spoilers.load(p)


UNPUBLISHED_SENTENCE = (
    "Nine people came into the hill that morning and only six of them "
    "walked back out again before the light failed."
)
PUBLISHED_SENTENCE = (
    "This is a sentence that only ever appeared in the published run of "
    "scenes and nowhere else in the unpublished drafts at all."
)
SHARED_SENTENCE = (
    "This exact sentence appears in both the published run and an early "
    "unpublished draft because a scene was reused essentially unchanged."
)
SHORT_SENTENCE = "Halla walked home."  # under 7 words


@pytest.fixture()
def index():
    idx = prose_index.ProseIndex(shingle_size=7)
    idx.unpublished = prose_index.shingle_hashes(UNPUBLISHED_SENTENCE)
    idx.unpublished |= prose_index.shingle_hashes(SHARED_SENTENCE)
    idx.published = prose_index.shingle_hashes(PUBLISHED_SENTENCE)
    idx.published |= prose_index.shingle_hashes(SHARED_SENTENCE)
    idx.unpublished_only = idx.unpublished - idx.published
    return idx


def test_quoted_unpublished_sentence_is_redacted(spoilers, index):
    counts = redact.RedactionCounts()
    out = redact.redact_text(
        f"The subagent wrote: {UNPUBLISHED_SENTENCE}", spoilers, counts, index
    )
    assert "Nine people" not in out
    assert "⟦redacted sentence: unpublished prose⟧" in out
    assert counts.by_category["prose_guard:unpublished_quote"] == 1


def test_quoted_published_sentence_is_left_alone(spoilers, index):
    counts = redact.RedactionCounts()
    out = redact.redact_text(
        f"The subagent wrote: {PUBLISHED_SENTENCE}", spoilers, counts, index
    )
    assert PUBLISHED_SENTENCE in out
    assert "prose_guard:unpublished_quote" not in counts.by_category


def test_sentence_shared_by_both_is_not_redacted(spoilers, index):
    # Present in the published run too, so quoting it isn't a spoiler even
    # though it's also technically "in" the unpublished set.
    counts = redact.RedactionCounts()
    out = redact.redact_text(SHARED_SENTENCE, spoilers, counts, index)
    assert SHARED_SENTENCE in out
    assert "prose_guard:unpublished_quote" not in counts.by_category


def test_short_sentence_cannot_match(spoilers, index):
    counts = redact.RedactionCounts()
    out = redact.redact_text(SHORT_SENTENCE, spoilers, counts, index)
    assert out == SHORT_SENTENCE
    assert "prose_guard:unpublished_quote" not in counts.by_category


def test_guard_disabled_when_no_index_given(spoilers):
    counts = redact.RedactionCounts()
    out = redact.redact_text(UNPUBLISHED_SENTENCE, spoilers, counts, None)
    assert out == UNPUBLISHED_SENTENCE


def test_only_the_quoting_sentence_is_redacted_not_neighbours(spoilers, index):
    counts = redact.RedactionCounts()
    text = f"Before it. {UNPUBLISHED_SENTENCE} After it stays visible."
    out = redact.redact_text(text, spoilers, counts, index)
    assert "Before it." in out
    assert "After it stays visible." in out
    assert "⟦redacted sentence: unpublished prose⟧" in out


def test_load_prose_index_returns_none_when_missing(tmp_path):
    assert redact.load_prose_index(tmp_path / "nope.pkl") is None


def test_load_prose_index_precomputes_unpublished_only(tmp_path):
    idx = prose_index.ProseIndex(shingle_size=7)
    idx.unpublished = {b"\x01" * 8, b"\x02" * 8}
    idx.published = {b"\x02" * 8}
    path = tmp_path / "index.pkl"
    idx.save(path)
    loaded = redact.load_prose_index(path)
    assert loaded.unpublished_only == {b"\x01" * 8}


def test_redact_transcript_threads_prose_index(spoilers, index):
    doc = {
        "session_id": "abc",
        "turns": [
            {
                "role": "assistant",
                "blocks": [
                    {"kind": "text", "text": UNPUBLISHED_SENTENCE},
                    {
                        "kind": "tool_result",
                        "stdout_preview": [UNPUBLISHED_SENTENCE],
                    },
                ],
            }
        ],
    }
    redacted, counts = redact.redact_transcript(doc, spoilers, index)
    all_text = json.dumps(redacted)
    assert "Nine people" not in all_text
    assert counts.by_category["prose_guard:unpublished_quote"] == 2
