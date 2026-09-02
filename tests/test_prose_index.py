import subprocess
from datetime import datetime, timezone

import pytest

from tools import prose_index


def _git(repo, *args, date=None):
    env = None
    if date is not None:
        import os

        env = dict(os.environ)
        env["GIT_AUTHOR_DATE"] = date
        env["GIT_COMMITTER_DATE"] = date
    subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, env=env
    )


@pytest.fixture()
def fake_novel_repo(tmp_path, monkeypatch):
    repo = tmp_path / "novel"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")

    chapters = repo / "chapters"
    chapters.mkdir()

    # A file added well before the cutoff -- should be excluded.
    old_words = " ".join(f"oldword{i}" for i in range(20))
    (chapters / "old.md").write_text(old_words)
    _git(repo, "add", "chapters/old.md")
    _git(repo, "commit", "-q", "-m", "old", date="2026-08-24T10:00:00+00:00")

    # A file added well after the cutoff -- should be kept.
    new_words = " ".join(f"newword{i}" for i in range(20))
    (chapters / "new.md").write_text(new_words)
    _git(repo, "add", "chapters/new.md")
    _git(repo, "commit", "-q", "-m", "new", date="2026-08-25T10:00:00+00:00")

    monkeypatch.setattr(prose_index, "AUTOROAD_ROOT", repo)
    monkeypatch.setattr(prose_index, "SCENES_DIR", repo / "no-such-scenes-dir")
    monkeypatch.setattr(prose_index, "UNPUBLISHED_TREE_GLOBS", [])
    monkeypatch.setattr(
        prose_index,
        "_load_premise_cutoff",
        lambda: datetime(2026, 8, 24, 13, 11, 27, tzinfo=timezone.utc),
    )
    return repo


def test_normalise_lowercases_strips_punctuation_collapses_whitespace():
    text = "Edwin,  said:  \"The   Bittle   is   gone!\"\n\nReally."
    assert prose_index.normalise(text) == "edwin said the bittle is gone really"


def test_shingle_hashes_empty_for_short_text():
    assert prose_index.shingle_hashes("only six words here right now", n=7) == set()


def test_shingle_hashes_nonempty_for_long_enough_text():
    hashes = prose_index.shingle_hashes(
        "the quick brown fox jumps over the lazy dog today", n=7
    )
    assert len(hashes) == 4  # 10 words - 7 + 1


def test_shingle_hashes_deterministic():
    text = "Nine people came into it and only six people came out again."
    assert prose_index.shingle_hashes(text) == prose_index.shingle_hashes(text)


def test_shingle_hashes_insensitive_to_case_and_punctuation():
    a = prose_index.shingle_hashes("Nine people came into it, and only six left.")
    b = prose_index.shingle_hashes("nine people came into it and only six left")
    assert a == b


def test_shingle_hashes_differ_for_different_text():
    a = prose_index.shingle_hashes("the quick brown fox jumps over the lazy dog")
    b = prose_index.shingle_hashes("a slow green frog hops under a sleepy cat")
    assert a.isdisjoint(b)


def test_build_index_excludes_pre_cutoff_blobs_but_keeps_post_cutoff_ones(
    fake_novel_repo,
):
    index = prose_index.build_index()
    old_hashes = prose_index.shingle_hashes(
        " ".join(f"oldword{i}" for i in range(20))
    )
    new_hashes = prose_index.shingle_hashes(
        " ".join(f"newword{i}" for i in range(20))
    )
    assert old_hashes.isdisjoint(index.unpublished)
    assert new_hashes & index.unpublished == new_hashes
    assert index.excluded_pre_cutoff_blobs == 1


def test_prose_index_roundtrips_through_pickle(tmp_path):
    index = prose_index.ProseIndex(shingle_size=7)
    index.unpublished = {b"\x01" * 8, b"\x02" * 8}
    index.published = {b"\x02" * 8, b"\x03" * 8}
    index.unpublished_source_count = 3
    index.published_source_count = 1
    path = tmp_path / "index.pkl"
    index.save(path)
    loaded = prose_index.ProseIndex.load(path)
    assert loaded.unpublished == index.unpublished
    assert loaded.published == index.published
    assert loaded.shingle_size == 7
