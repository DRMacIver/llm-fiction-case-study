"""Tests for tools/voice_lint.py."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.voice_lint import lint_text, PAGES_UNDER_CHECK  # noqa: E402


def _tiers(report, tier):
    return [f for f in report.findings if f.tier == tier]


def test_fail_vocabulary_detected():
    report = lint_text(Path("x.md"), "The system continued to delve into the archive.")
    assert any("delve" in f.note.lower() for f in _tiers(report, "FAIL"))


def test_earn_its_keep_is_fail():
    report = lint_text(Path("x.md"), "The linter earns its keep on its own.")
    assert _tiers(report, "FAIL")


def test_in_the_plain_sense_is_fail():
    report = lint_text(Path("x.md"), "That is hallucination in the plain sense.")
    assert _tiers(report, "FAIL")


def test_which_is_most_of_why_is_fail():
    report = lint_text(Path("x.md"), "It cross-links a lot, which is most of why it works.")
    assert _tiers(report, "FAIL")


def test_generic_h2_header_is_fail():
    report = lint_text(Path("x.md"), "## Conclusion\n\nSome text.")
    assert any("generic header" in f.note for f in _tiers(report, "FAIL"))


def test_introduction_h1_is_not_flagged():
    # This site uses "# Introduction" as a legitimate page title.
    report = lint_text(Path("introduction.md"), "# Introduction\n\nSome text.")
    assert not any("generic header" in f.note for f in report.findings)


def test_bold_in_prose_is_review():
    report = lint_text(Path("x.md"), "This is **very important** to know.")
    assert any("bold" in f.note.lower() for f in _tiers(report, "REVIEW"))


def test_em_dash_is_review():
    report = lint_text(Path("x.md"), "The project was ambitious — too ambitious.")
    assert any("em dash" in f.note.lower() for f in _tiers(report, "REVIEW"))


def test_semicolon_is_review():
    report = lint_text(Path("x.md"), "The checker ran; it found nothing.")
    assert any("semicolon" in f.note.lower() for f in _tiers(report, "REVIEW"))


def test_worth_noting_is_review():
    report = lint_text(Path("x.md"), "It's worth noting that this ran quickly.")
    assert any("importance-narration" in f.note for f in _tiers(report, "REVIEW"))


def test_negative_parallelism_is_review():
    report = lint_text(
        Path("x.md"),
        "It wasn't a formatting problem. It was a voice problem.",
    )
    assert any("negative parallelism" in f.note for f in _tiers(report, "REVIEW"))


def test_verdict_clause_is_review():
    report = lint_text(
        Path("x.md"),
        "It fixed the bug quickly, which was the point.",
    )
    assert any("verdict clause" in f.note for f in _tiers(report, "REVIEW"))


def test_code_fence_is_not_scanned():
    text = "Some prose.\n\n```\ndelve into archive\n```\n\nMore prose."
    report = lint_text(Path("x.md"), text)
    assert not _tiers(report, "FAIL")


def test_inline_code_is_not_scanned():
    report = lint_text(Path("x.md"), "Run `delve into archive` to see it.")
    assert not any("delve" in f.note.lower() for f in _tiers(report, "FAIL"))


def test_link_target_not_scanned_as_prose():
    text = "See [this page](delve-into-archive.md) for more."
    report = lint_text(Path("x.md"), text)
    assert not any("delve" in f.note.lower() for f in _tiers(report, "FAIL"))


def test_clean_prose_has_no_fail():
    text = (
        "The linter caught a great deal of drift early. It runs in seconds "
        "and never disagrees with itself, which made it easy to trust."
    )
    report = lint_text(Path("x.md"), text)
    assert not _tiers(report, "FAIL")


def test_info_stats_present():
    report = lint_text(Path("x.md"), "This is a short sentence. Here is another one.")
    joined = " ".join(report.info)
    assert "words:" in joined
    assert "em dashes:" in joined
    assert "sentences:" in joined


def test_pages_under_check_all_exist():
    assert PAGES_UNDER_CHECK, "expected at least one page to check"
    for path in PAGES_UNDER_CHECK:
        assert path.exists(), path
