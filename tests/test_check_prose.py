import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import check_prose


def test_check_links_flags_missing_target(tmp_path):
    page = tmp_path / "a.md"
    page.write_text("See [good](b.md) and [bad](missing.md).\n")
    (tmp_path / "b.md").write_text("# B\n")
    orig_root = check_prose.REPO_ROOT
    try:
        check_prose.REPO_ROOT = tmp_path
        results = check_prose.check_links({"a.md": page.read_text()})
    finally:
        check_prose.REPO_ROOT = orig_root

    by_target = {r.target: r for r in results}
    assert by_target["b.md"].ok is True
    assert by_target["missing.md"].ok is False


def test_check_links_ignores_absolute_and_anchor_links(tmp_path):
    page = tmp_path / "a.md"
    text = "[ext](https://example.com/x) and [anchor](#section) and [mail](mailto:x@example.com)\n"
    page.write_text(text)
    orig_root = check_prose.REPO_ROOT
    try:
        check_prose.REPO_ROOT = tmp_path
        results = check_prose.check_links({"a.md": text})
    finally:
        check_prose.REPO_ROOT = orig_root
    assert results == []


def test_check_links_with_fragment_on_real_file(tmp_path):
    page = tmp_path / "a.md"
    (tmp_path / "b.md").write_text("# B\n")
    text = "[frag](b.md#heading)\n"
    page.write_text(text)
    orig_root = check_prose.REPO_ROOT
    try:
        check_prose.REPO_ROOT = tmp_path
        results = check_prose.check_links({"a.md": text})
    finally:
        check_prose.REPO_ROOT = orig_root
    assert len(results) == 1
    assert results[0].ok is True


def test_extract_numbers_finds_digits_and_words():
    pages = {
        "p.md": "There were three sessions and 625 commits, but 2026 is not a count.\n"
    }
    mentions, dates = check_prose.extract_numbers(pages)
    values = {m.value for m in mentions}
    assert 3 in values
    assert 625 in values
    assert 2026 not in values  # year should be excluded


def test_extract_numbers_tags_topics():
    pages = {"p.md": "The book has eighteen chapters and 40 scenes.\n"}
    mentions, _ = check_prose.extract_numbers(pages)
    topics_by_value = {m.value: m.topics for m in mentions}
    assert "chapter" in topics_by_value[18]
    assert "scene" in topics_by_value[40]


def test_extract_dates_flags_out_of_range():
    pages = {"p.md": "Work began on 2026-08-24 and something odd happened on 2026-09-15.\n"}
    _, dates = check_prose.extract_numbers(pages)
    ok_dates = {d.raw: d.ok for d in dates}
    assert ok_dates["2026-08-24"] is True
    assert ok_dates["2026-09-15"] is False


def test_parse_number_handles_words_and_digits():
    assert check_prose.parse_number("three") == 3
    assert check_prose.parse_number("dozen") == 12
    assert check_prose.parse_number("2,000") == 2000
    assert check_prose.parse_number("notanumber") is None
